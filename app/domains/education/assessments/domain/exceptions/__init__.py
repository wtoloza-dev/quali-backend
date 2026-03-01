"""Assessments subdomain domain exceptions."""

from .max_attempts_exceeded_exception import MaxAttemptsExceededException
from .question_not_found_exception import QuestionNotFoundException


__all__ = ["QuestionNotFoundException", "MaxAttemptsExceededException"]
