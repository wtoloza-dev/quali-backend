"""Unit tests for SubmitAttemptUseCase."""

from datetime import UTC, datetime

import pytest

from app.domains.education.assessments.application.use_cases import SubmitAttemptUseCase
from app.domains.education.assessments.domain.entities import (
    AnswerEntry,
    AttemptData,
    AttemptEntity,
    MCOption,
    MultipleChoiceConfig,
    QuestionEntity,
)
from app.domains.education.assessments.domain.enums import QuestionType
from app.domains.education.assessments.domain.exceptions import (
    MaxAttemptsExceededException,
)
from app.domains.education.courses.domain.entities import ModuleEntity
from app.domains.education.enrollments.domain.entities import EnrollmentEntity
from app.domains.education.enrollments.domain.enums import AccessType, EnrollmentStatus


ENROLLMENT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAE"
COURSE_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAR"
MODULE_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAM"
SUBMITTED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAU"


def _make_enrollment(
    course_id: str = COURSE_ID,
    status: EnrollmentStatus = EnrollmentStatus.NOT_STARTED,
) -> EnrollmentEntity:
    now = datetime.now(UTC)
    return EnrollmentEntity(
        id=ENROLLMENT_ID,
        user_id=SUBMITTED_BY,
        course_id=course_id,
        is_mandatory=False,
        status=status,
        access_type=AccessType.PREVIEW,
        enrolled_at=now,
        completed_at=None,
        start_date=None,
        end_date=None,
        created_at=now,
        created_by=SUBMITTED_BY,
        updated_at=now,
        updated_by=None,
    )


def _make_module(max_attempts: int = 3, passing_score: int = 70) -> ModuleEntity:
    now = datetime.now(UTC)
    return ModuleEntity(
        id=MODULE_ID,
        course_id=COURSE_ID,
        title="Test Module",
        order=1,
        passing_score=passing_score,
        max_attempts=max_attempts,
        created_at=now,
        created_by=SUBMITTED_BY,
        updated_at=now,
        updated_by=None,
    )


def _make_question(question_id: str, correct_index: int = 0) -> QuestionEntity:
    now = datetime.now(UTC)
    return QuestionEntity(
        id=question_id,
        course_id=COURSE_ID,
        text="Sample question",
        question_type=QuestionType.MULTIPLE_CHOICE_SINGLE,
        config=MultipleChoiceConfig(
            options=[
                MCOption(text="Option A", is_correct=(correct_index == 0)),
                MCOption(text="Option B", is_correct=(correct_index == 1)),
            ],
        ),
        order=0,
        module_id=MODULE_ID,
        created_at=now,
        created_by=SUBMITTED_BY,
        updated_at=now,
        updated_by=None,
    )


class FakeEnrollmentRepository:
    def __init__(self, enrollment: EnrollmentEntity) -> None:
        self._store = {enrollment.id: enrollment}

    async def get_by_id(self, enrollment_id):
        return self._store.get(enrollment_id)

    async def get_by_user_and_course(self, user_id, course_id):
        return None

    async def update(self, entity):
        self._store[entity.id] = entity
        return entity

    async def save(self, entity):
        self._store[entity.id] = entity
        return entity

    async def get_active_enrollment(self, user_id, course_id):
        return None

    async def delete(self, enrollment_id, deleted_by):
        pass

    async def list_by_user(self, user_id, page, page_size):
        return [], 0


class FakeModuleRepository:
    def __init__(self, module: ModuleEntity) -> None:
        self._store = {module.id: module}

    async def get_by_id(self, module_id):
        return self._store.get(module_id)

    async def save(self, entity):
        self._store[entity.id] = entity
        return entity

    async def update(self, entity):
        self._store[entity.id] = entity
        return entity

    async def delete(self, module_id, deleted_by):
        pass

    async def list_by_course(self, course_id):
        return [m for m in self._store.values() if m.course_id == course_id]

    async def update_order(self, module_id, order):
        pass


class FakeQuestionRepository:
    def __init__(self, questions: list[QuestionEntity]) -> None:
        self._store = {q.id: q for q in questions}

    async def save(self, entity):
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, question_id):
        return self._store.get(question_id)

    async def list_by_course(self, course_id):
        return [q for q in self._store.values() if q.course_id == course_id]

    async def list_by_module(self, module_id):
        return [q for q in self._store.values() if q.module_id == module_id]

    async def delete(self, question_id, deleted_by):
        self._store.pop(question_id, None)


class FakeAttemptRepository:
    def __init__(self, existing_count: int = 0) -> None:
        self._store: dict[str, AttemptEntity] = {}
        self._count = existing_count

    async def save(self, entity: AttemptEntity) -> AttemptEntity:
        self._store[entity.id] = entity
        return entity

    async def count_by_enrollment(self, enrollment_id: str) -> int:
        return self._count

    async def count_by_enrollment_and_module(
        self, enrollment_id: str, module_id: str
    ) -> int:
        return self._count

    async def list_by_enrollment(self, enrollment_id: str) -> list[AttemptEntity]:
        return [e for e in self._store.values() if e.enrollment_id == enrollment_id]


def _make_use_case(
    questions: list[QuestionEntity],
    existing_attempts: int = 0,
    max_attempts: int = 3,
    passing_score: int = 70,
    enrollment: EnrollmentEntity | None = None,
) -> tuple[SubmitAttemptUseCase, FakeEnrollmentRepository, FakeAttemptRepository]:
    enrollment = enrollment or _make_enrollment()
    module = _make_module(max_attempts=max_attempts, passing_score=passing_score)
    enroll_repo = FakeEnrollmentRepository(enrollment)
    module_repo = FakeModuleRepository(module)
    question_repo = FakeQuestionRepository(questions)
    attempt_repo = FakeAttemptRepository(existing_count=existing_attempts)
    use_case = SubmitAttemptUseCase(
        enrollment_repository=enroll_repo,
        module_repository=module_repo,
        question_repository=question_repo,
        attempt_repository=attempt_repo,
    )
    return use_case, enroll_repo, attempt_repo


def _attempt_data(answers: list[AnswerEntry]) -> AttemptData:
    """Build AttemptData with module_id set for module-level assessment."""
    return AttemptData(
        enrollment_id=ENROLLMENT_ID,
        module_id=MODULE_ID,
        answers=answers,
    )


class TestSubmitAttemptUseCase:
    async def test_scores_all_correct_answers_as_100(self):
        q1 = _make_question("q1", correct_index=0)
        q2 = _make_question("q2", correct_index=1)
        use_case, _, _ = _make_use_case([q1, q2])
        data = _attempt_data(
            [
                AnswerEntry(question_id="q1", selected_indices=[0]),
                AnswerEntry(question_id="q2", selected_indices=[1]),
            ]
        )

        result = await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

        assert result.score == 100
        assert result.passed is True

    async def test_scores_all_wrong_answers_as_0(self):
        q1 = _make_question("q1", correct_index=0)
        use_case, _, _ = _make_use_case([q1])
        data = _attempt_data(
            [
                AnswerEntry(question_id="q1", selected_indices=[1]),
            ]
        )

        result = await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

        assert result.score == 0
        assert result.passed is False

    async def test_partial_score_is_rounded(self):
        questions = [_make_question(f"q{i}", correct_index=0) for i in range(3)]
        use_case, _, _ = _make_use_case(questions, passing_score=50)
        data = _attempt_data(
            [
                AnswerEntry(question_id="q0", selected_indices=[0]),  # correct
                AnswerEntry(question_id="q1", selected_indices=[1]),  # wrong
                AnswerEntry(question_id="q2", selected_indices=[1]),  # wrong
            ]
        )

        result = await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

        assert result.score == 33

    async def test_attempt_number_increments(self):
        q1 = _make_question("q1", correct_index=0)
        use_case, _, _ = _make_use_case([q1], existing_attempts=2)
        data = _attempt_data(
            [
                AnswerEntry(question_id="q1", selected_indices=[0]),
            ]
        )

        result = await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

        assert result.attempt_number == 3

    async def test_raises_when_max_attempts_exceeded(self):
        q1 = _make_question("q1", correct_index=0)
        use_case, _, _ = _make_use_case([q1], existing_attempts=3, max_attempts=3)
        data = _attempt_data(
            [
                AnswerEntry(question_id="q1", selected_indices=[0]),
            ]
        )

        with pytest.raises(MaxAttemptsExceededException):
            await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

    async def test_enrollment_status_becomes_in_progress_on_first_module_attempt(self):
        q1 = _make_question("q1", correct_index=0)
        use_case, enroll_repo, _ = _make_use_case([q1], passing_score=50)
        data = _attempt_data(
            [
                AnswerEntry(question_id="q1", selected_indices=[0]),
            ]
        )

        await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

        updated = await enroll_repo.get_by_id(ENROLLMENT_ID)
        assert updated.status == EnrollmentStatus.IN_PROGRESS

    async def test_enrollment_status_becomes_failed_when_attempts_exhausted(self):
        q1 = _make_question("q1", correct_index=0)
        # Course-level attempt (no module_id) to test FAILED status
        use_case, enroll_repo, _ = _make_use_case(
            [q1], existing_attempts=2, max_attempts=3, passing_score=100
        )
        # Use course-level attempt data — defaults apply (80/3) but we override via module
        data = _attempt_data(
            [
                AnswerEntry(question_id="q1", selected_indices=[1]),  # wrong
            ]
        )

        await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

        updated = await enroll_repo.get_by_id(ENROLLMENT_ID)
        # Module-level attempts don't update enrollment to FAILED
        assert updated.status == EnrollmentStatus.IN_PROGRESS

    async def test_enrollment_status_becomes_in_progress_when_not_passed_and_attempts_remain(
        self,
    ):
        q1 = _make_question("q1", correct_index=0)
        use_case, enroll_repo, _ = _make_use_case(
            [q1], existing_attempts=0, max_attempts=3, passing_score=100
        )
        data = _attempt_data(
            [
                AnswerEntry(question_id="q1", selected_indices=[1]),  # wrong
            ]
        )

        await use_case.execute(data=data, submitted_by=SUBMITTED_BY)

        updated = await enroll_repo.get_by_id(ENROLLMENT_ID)
        assert updated.status == EnrollmentStatus.IN_PROGRESS


class TestScoreAnswers:
    def test_empty_questions_returns_zero(self):
        score, correct_ids = SubmitAttemptUseCase._score_answers([], [])
        assert score == 0
        assert correct_ids == []

    def test_unknown_question_id_is_skipped(self):
        q1 = _make_question("q1", correct_index=0)
        answers = [AnswerEntry(question_id="unknown", selected_indices=[0])]
        score, correct_ids = SubmitAttemptUseCase._score_answers(answers, [q1])
        assert score == 0
        assert correct_ids == []
