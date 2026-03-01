"""Assessment attempt domain entity."""

from datetime import datetime

from pydantic import BaseModel

from app.shared.entities import AuditEntity


class AnswerEntry(BaseModel):
    """A single answer submitted by a student.

    Attributes:
        question_id: ULID of the question being answered.
        selected_indices: Zero-based indices of the selected options (MC/TF).
        found_words: List of words found by the student (word_search).
        cell_answers: Map of "row,col" → letter for crossword answers.
    """

    question_id: str
    selected_indices: list[int] = []
    found_words: list[str] = []
    cell_answers: dict[str, str] = {}


class AttemptData(BaseModel):
    """Input fields required to submit an assessment attempt.

    Attributes:
        enrollment_id: ULID of the enrollment this attempt belongs to.
        answers: List of answers, one per question.
    """

    enrollment_id: str
    module_id: str | None = None
    answers: list[AnswerEntry]


class AttemptEntity(AuditEntity):
    """Full persisted assessment attempt record.

    Attributes:
        enrollment_id: ULID of the enrollment this attempt belongs to.
        score: Percentage score (0–100).
        passed: Whether the score met the course passing threshold.
        attempt_number: Sequential attempt number for this enrollment (1-based).
        answers: Snapshot of the answers submitted.
        taken_at: Timestamp when the attempt was submitted.
    """

    enrollment_id: str
    module_id: str | None = None
    score: int
    passed: bool
    attempt_number: int
    answers: list[AnswerEntry]
    correct_question_ids: list[str] = []
    taken_at: datetime
