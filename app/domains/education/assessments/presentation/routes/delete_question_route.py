"""Delete assessment question route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import DeleteQuestionUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{course_id}/questions/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a question from a course's question bank",
)
async def handle_delete_question_route(
    company_id: str,
    course_id: str,
    question_id: str,
    use_case: DeleteQuestionUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle DELETE requests to remove a question.

    Args:
        company_id: ULID of the owning company (from URL path).
        course_id: ULID of the parent course (from URL path).
        question_id: ULID of the question to delete.
        use_case: Injected DeleteQuestionUseCase.
        auth: Authenticated user context.
    """
    await use_case.execute(
        question_id=question_id,
        course_id=course_id,
        company_id=company_id,
        deleted_by=auth.user_id,
    )
