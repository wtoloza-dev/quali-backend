"""Assessment question domain entity."""

from __future__ import annotations

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import QuestionType
from .question_config import MultipleChoiceConfig, QuestionConfig


class QuestionData(BaseModel):
    """Input fields required to create a question.

    The ``config`` field is a Pydantic discriminated union: the correct
    sub-schema is selected automatically based on the ``type`` key inside
    the config dict (``multiple_choice``, ``word_search``, or ``crossword``).
    """

    course_id: str
    module_id: str | None = None
    text: str
    question_type: QuestionType
    config: QuestionConfig = MultipleChoiceConfig()
    randomize: bool = True
    order: int = 0


class QuestionEntity(QuestionData, AuditEntity):
    """Full persisted question record."""


__all__ = [
    "QuestionConfig",
    "QuestionData",
    "QuestionEntity",
]
