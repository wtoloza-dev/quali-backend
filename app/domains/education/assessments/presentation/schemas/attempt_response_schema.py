"""Assessment attempt response schema."""

from datetime import datetime

from pydantic import BaseModel


class AnswerEntryResponseSchema(BaseModel):
    """A submitted answer in the response.

    Attributes:
        question_id: ULID of the question.
        selected_indices: Indices of the options the student selected.
    """

    question_id: str
    selected_indices: list[int] = []
    found_words: list[str] = []
    cell_answers: dict[str, str] = {}


class AttemptResponseSchema(BaseModel):
    """Full attempt response.

    Attributes:
        id: ULID of the attempt.
        enrollment_id: ULID of the parent enrollment.
        score: Percentage score (0–100).
        passed: Whether the score met the passing threshold.
        attempt_number: Sequential attempt number (1-based).
        answers: Snapshot of submitted answers.
        taken_at: Timestamp when the attempt was submitted.
        created_at: Audit timestamp.
    """

    id: str
    enrollment_id: str
    module_id: str | None = None
    score: int
    passed: bool
    attempt_number: int
    answers: list[AnswerEntryResponseSchema]
    correct_question_ids: list[str] = []
    taken_at: datetime
    created_at: datetime
