"""Submit attempt request schema."""

from pydantic import BaseModel


class AnswerEntrySchema(BaseModel):
    """A single submitted answer.

    Attributes:
        question_id: ULID of the question being answered.
        selected_indices: Zero-based indices of the selected options.
    """

    question_id: str
    selected_indices: list[int] = []
    found_words: list[str] = []
    cell_answers: dict[str, str] = {}
    sorted_indices: list[int] = []
    classified_items: dict[str, int] = {}
    matched_pairs: dict[str, str] = {}


class SubmitAttemptRequestSchema(BaseModel):
    """Request body for submitting an assessment attempt.

    Attributes:
        answers: One answer entry per question in the assessment.
    """

    module_id: str | None = None
    answers: list[AnswerEntrySchema]
