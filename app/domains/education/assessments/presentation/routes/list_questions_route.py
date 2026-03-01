"""List assessment questions route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import ListQuestionsUseCaseDependency
from ..mappers.question_mapper import QuestionMapper
from ..schemas.question_response_schema import QuestionResponseSchema


router = APIRouter()


@router.get(
    path="/{course_id}/questions",
    status_code=status.HTTP_200_OK,
    summary="List all questions in a course's question bank",
)
async def handle_list_questions_route(
    company_id: str,
    course_id: str,
    use_case: ListQuestionsUseCaseDependency,
    auth: CurrentUserDependency,  # noqa: ARG001 — auth guard
) -> list[QuestionResponseSchema]:
    """Handle GET requests to list all questions for a course.

    Args:
        company_id: ULID of the owning company (from URL path).
        course_id: ULID of the course (from URL path).
        use_case: Injected ListQuestionsUseCase.
        auth: Authenticated user context (required, not used directly).

    Returns:
        list[QuestionResponseSchema]: All questions ordered by display order.
    """
    entities = await use_case.execute(
        course_id=course_id,
        company_id=company_id,
    )
    return [QuestionMapper.to_response(e) for e in entities]
