"""Delete lesson route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import DeleteLessonUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{course_id}/modules/{module_id}/lessons/{lesson_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a lesson",
    description="Hard-deletes a lesson.",
)
async def handle_delete_lesson_route(
    company_id: str,
    course_id: str,
    module_id: str,
    lesson_id: str,
    use_case: DeleteLessonUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle DELETE requests to remove a lesson.

    Args:
        company_id: ULID of the owning company from the URL path.
        course_id: ULID of the parent course.
        module_id: ULID of the parent module.
        lesson_id: ULID of the lesson to delete.
        use_case: Injected DeleteLessonUseCase.
        auth: Authenticated user context.
    """
    await use_case.execute(
        course_id=course_id,
        company_id=company_id,
        module_id=module_id,
        lesson_id=lesson_id,
        deleted_by=auth.user_id,
    )
