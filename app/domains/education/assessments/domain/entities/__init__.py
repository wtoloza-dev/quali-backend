"""Assessments subdomain domain entities."""

from .attempt_entity import AnswerEntry, AttemptData, AttemptEntity
from .question_config import (
    ClassificationCategory,
    ClassificationConfig,
    ClassificationItem,
    CrosswordClue,
    CrosswordConfig,
    MatchingConfig,
    MatchingPair,
    MCOption,
    MultipleChoiceConfig,
    QuestionConfig,
    SortingConfig,
    WordPosition,
    WordSearchConfig,
)
from .question_entity import QuestionData, QuestionEntity


__all__ = [
    "AnswerEntry",
    "AttemptData",
    "AttemptEntity",
    "ClassificationCategory",
    "ClassificationConfig",
    "ClassificationItem",
    "CrosswordClue",
    "CrosswordConfig",
    "MatchingConfig",
    "MatchingPair",
    "MCOption",
    "MultipleChoiceConfig",
    "QuestionConfig",
    "QuestionData",
    "QuestionEntity",
    "SortingConfig",
    "WordPosition",
    "WordSearchConfig",
]
