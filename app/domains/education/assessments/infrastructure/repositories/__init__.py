"""Assessments subdomain repositories."""

from .attempt_repository import AttemptRepository
from .question_repository import QuestionRepository


__all__ = ["QuestionRepository", "AttemptRepository"]
