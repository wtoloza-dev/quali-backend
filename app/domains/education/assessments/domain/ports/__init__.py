"""Assessments subdomain domain ports."""

from .attempt_repository_port import AttemptRepositoryPort
from .question_repository_port import QuestionRepositoryPort


__all__ = ["QuestionRepositoryPort", "AttemptRepositoryPort"]
