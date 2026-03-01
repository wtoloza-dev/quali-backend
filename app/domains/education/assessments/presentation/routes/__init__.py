"""Assessments subdomain route handlers.

Questions are nested under /courses/{course_id}/questions.
Attempts are nested under /enrollments/{enrollment_id}/attempts.
"""

from fastapi import APIRouter

from .create_question_route import router as create_question_router
from .delete_question_route import router as delete_question_router
from .list_attempts_route import router as list_attempts_router
from .list_module_questions_route import router as list_module_questions_router
from .list_questions_route import router as list_questions_router
from .submit_attempt_route import router as submit_attempt_router


questions_router = APIRouter()
questions_router.include_router(list_questions_router)
questions_router.include_router(list_module_questions_router)
questions_router.include_router(create_question_router)
questions_router.include_router(delete_question_router)

attempts_router = APIRouter()
attempts_router.include_router(list_attempts_router)
attempts_router.include_router(submit_attempt_router)

__all__ = ["questions_router", "attempts_router"]
