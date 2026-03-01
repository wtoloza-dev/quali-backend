"""Assessments subdomain domain entities."""

from .attempt_entity import AnswerEntry, AttemptData, AttemptEntity
from .question_config import (
    CrosswordClue,
    CrosswordConfig,
    MCOption,
    MultipleChoiceConfig,
    QuestionConfig,
    WordPosition,
    WordSearchConfig,
)
from .question_entity import QuestionData, QuestionEntity


__all__ = [
    "AnswerEntry",
    "AttemptData",
    "AttemptEntity",
    "CrosswordClue",
    "CrosswordConfig",
    "MCOption",
    "MultipleChoiceConfig",
    "QuestionConfig",
    "QuestionData",
    "QuestionEntity",
    "WordPosition",
    "WordSearchConfig",
]
