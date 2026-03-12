"""Submit assessment attempt use case."""

from datetime import UTC, datetime

from ulid import ULID

from app.domains.education.courses.domain.ports import CourseRepositoryPort
from app.domains.education.enrollments.domain.enums import EnrollmentStatus
from app.domains.education.enrollments.domain.ports import EnrollmentRepositoryPort

from ...domain.entities import (
    AnswerEntry,
    AttemptData,
    AttemptEntity,
    CrosswordConfig,
    MultipleChoiceConfig,
    QuestionEntity,
    WordSearchConfig,
    SortingConfig,
    ClassificationConfig,
    MatchingConfig,
)
from ...domain.exceptions import MaxAttemptsExceededException
from ...domain.ports import AttemptRepositoryPort, QuestionRepositoryPort


class SubmitAttemptUseCase:
    """Score and persist a student's assessment attempt.

    Supports both course-level and per-module assessments. When module_id
    is provided in the attempt data, only that module's questions are used
    for scoring and attempt counting.
    """

    def __init__(
        self,
        enrollment_repository: EnrollmentRepositoryPort,
        course_repository: CourseRepositoryPort,
        question_repository: QuestionRepositoryPort,
        attempt_repository: AttemptRepositoryPort,
    ) -> None:
        self._enrollments = enrollment_repository
        self._courses = course_repository
        self._questions = question_repository
        self._attempts = attempt_repository

    async def execute(
        self,
        data: AttemptData,
        submitted_by: str,
    ) -> AttemptEntity:
        """Grade and persist an assessment attempt."""
        enrollment = await self._enrollments.get_by_id(data.enrollment_id)
        course = await self._courses.get_by_id(enrollment.course_id)  # type: ignore[union-attr]

        max_attempts = course.max_attempts if course else 3  # type: ignore[union-attr]

        # Count attempts scoped to module when provided
        if data.module_id:
            existing_count = await self._attempts.count_by_enrollment_and_module(
                data.enrollment_id, data.module_id
            )
        else:
            existing_count = await self._attempts.count_by_enrollment(data.enrollment_id)

        if existing_count >= max_attempts:
            raise MaxAttemptsExceededException(
                enrollment_id=data.enrollment_id,
                max_attempts=max_attempts,
            )

        # Fetch questions scoped to module when provided
        if data.module_id:
            questions = await self._questions.list_by_module(module_id=data.module_id)
        else:
            questions = await self._questions.list_by_course(enrollment.course_id)  # type: ignore[union-attr]

        score, correct_question_ids = self._score_answers(data.answers, questions)

        passing_score = course.passing_score if course else 80  # type: ignore[union-attr]
        passed = score >= passing_score

        now = datetime.now(UTC)
        attempt = AttemptEntity(
            id=str(ULID()),
            enrollment_id=data.enrollment_id,
            module_id=data.module_id,
            score=score,
            passed=passed,
            attempt_number=existing_count + 1,
            answers=data.answers,
            correct_question_ids=correct_question_ids,
            taken_at=now,
            created_at=now,
            created_by=submitted_by,
            updated_at=None,
            updated_by=None,
        )
        saved_attempt = await self._attempts.save(attempt)

        # Update enrollment status (only for course-level or when module passes)
        if enrollment is not None and passed and not data.module_id:
            updated_enrollment = enrollment.model_copy(
                update={
                    "status": EnrollmentStatus.COMPLETED,
                    "completed_at": now,
                    "updated_by": submitted_by,
                }
            )
            await self._enrollments.update(updated_enrollment)
        elif enrollment is not None and not data.module_id:
            attempts_exhausted = (existing_count + 1) >= max_attempts
            if attempts_exhausted:
                new_status = EnrollmentStatus.FAILED
            else:
                new_status = EnrollmentStatus.IN_PROGRESS

            completed_at = enrollment.completed_at
            if new_status == EnrollmentStatus.FAILED:
                completed_at = now

            updated_enrollment = enrollment.model_copy(
                update={
                    "status": new_status,
                    "completed_at": completed_at,
                    "updated_by": submitted_by,
                }
            )
            await self._enrollments.update(updated_enrollment)

        return saved_attempt

    @staticmethod
    def _score_answers(
        answers: list[AnswerEntry],
        questions: list[QuestionEntity],
    ) -> tuple[int, list[str]]:
        """Calculate the percentage score and identify correct questions.

        Scores against submitted answers only (not total question bank).
        Supports multiple choice, word search, and crossword question types.

        Returns:
            Tuple of (percentage_score, list_of_correct_question_ids).
        """
        if not answers:
            return 0, []

        from ...domain.enums import QuestionType

        question_map = {q.id: q for q in questions}
        correct = 0
        answered = 0
        correct_question_ids: list[str] = []

        for answer in answers:
            question = question_map.get(answer.question_id)
            if question is None:
                continue

            answered += 1
            is_correct = False

            if question.question_type in (
                QuestionType.MULTIPLE_CHOICE_SINGLE,
                QuestionType.MULTIPLE_CHOICE_MULTI,
                QuestionType.TRUE_FALSE,
            ):
                cfg = question.config
                assert isinstance(cfg, MultipleChoiceConfig)
                correct_indices = {
                    i for i, opt in enumerate(cfg.options) if opt.is_correct
                }
                selected = set(answer.selected_indices)
                is_correct = selected == correct_indices

            elif question.question_type == QuestionType.WORD_SEARCH:
                cfg = question.config
                assert isinstance(cfg, WordSearchConfig)
                expected_words = {w.upper() for w in cfg.words}
                found = {w.upper() for w in answer.found_words}
                is_correct = found >= expected_words

            elif question.question_type == QuestionType.CROSSWORD:
                cfg = question.config
                assert isinstance(cfg, CrosswordConfig)
                expected: dict[str, str] = {}
                for clue in cfg.clues:
                    for i, char in enumerate(clue.answer.upper()):
                        if clue.direction == "across":
                            key = f"{clue.row},{clue.col + i}"
                        else:
                            key = f"{clue.row + i},{clue.col}"
                        expected[key] = char
                user_cells = {k: v.upper() for k, v in answer.cell_answers.items()}
                is_correct = all(
                    user_cells.get(k) == v for k, v in expected.items()
                )

            elif question.question_type == QuestionType.SORTING:
                cfg = question.config
                assert isinstance(cfg, SortingConfig)
                correct_order = list(range(len(cfg.items)))
                is_correct = answer.sorted_indices == correct_order

            elif question.question_type == QuestionType.CLASSIFICATION:
                cfg = question.config
                assert isinstance(cfg, ClassificationConfig)
                expected_class = {item.text.upper(): item.correct_category for item in cfg.items}
                student_class = {k.upper(): v for k, v in answer.classified_items.items()}
                is_correct = expected_class == student_class

            elif question.question_type == QuestionType.MATCHING:
                cfg = question.config
                assert isinstance(cfg, MatchingConfig)
                expected_match = {pair.left.upper(): pair.right.upper() for pair in cfg.pairs}
                student_match = {k.upper(): v.upper() for k, v in answer.matched_pairs.items()}
                is_correct = expected_match == student_match

            if is_correct:
                correct += 1
                correct_question_ids.append(answer.question_id)

        if answered == 0:
            return 0, []

        return round((correct / answered) * 100), correct_question_ids
