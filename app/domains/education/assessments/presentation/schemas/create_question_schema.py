"""Create question request schema."""

from pydantic import BaseModel

from ...domain.entities.question_config import MultipleChoiceConfig, QuestionConfig
from ...domain.enums import QuestionType


class CreateQuestionRequestSchema(BaseModel):
    """Request body for creating an assessment question.

    ``config`` is a discriminated union: include ``{"type": "multiple_choice", "options": [...]}``
    for MC/TF, ``{"type": "word_search", ...}`` or ``{"type": "crossword", ...}``.
    """

    text: str
    question_type: QuestionType
    config: QuestionConfig = MultipleChoiceConfig()
    randomize: bool = True
    order: int = 0
    module_id: str | None = None
