"""List assessment questions for a specific module."""

from fastapi import APIRouter, status

from ...infrastructure.dependencies import QuestionRepositoryDependency
from ..mappers.question_mapper import QuestionMapper
from ..schemas.question_response_schema import QuestionResponseSchema


router = APIRouter()


@router.get(
    path="/{course_id}/modules/{module_id}/questions",
    status_code=status.HTTP_200_OK,
    summary="List all questions for a specific module",
)
async def handle_list_module_questions_route(
    course_id: str,  # noqa: ARG001 — kept for URL consistency
    module_id: str,
    repository: QuestionRepositoryDependency,
) -> list[QuestionResponseSchema]:
    """Return all questions for a module.

    Public endpoint — no auth required (questions don't include answers
    in the response by default, but currently they do for dev/MVP).
    """
    entities = await repository.list_by_module(module_id=module_id)
    return [QuestionMapper.to_response(e) for e in entities]
