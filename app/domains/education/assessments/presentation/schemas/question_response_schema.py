"""Question response schema."""

from datetime import datetime

from pydantic import BaseModel

from ...domain.entities.question_config import MultipleChoiceConfig, QuestionConfig
from ...domain.enums import QuestionType


class QuestionResponseSchema(BaseModel):
    """Full question response for course managers."""

    id: str
    course_id: str
    module_id: str | None = None
    text: str
    question_type: QuestionType
    config: QuestionConfig = MultipleChoiceConfig()
    randomize: bool = True
    order: int
    created_at: datetime
    created_by: str
