"""Delete course route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import DeleteCourseUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a course",
    description="Hard-deletes a course. Only the owning company can delete.",
)
async def handle_delete_course_route(
    company_id: str,
    course_id: str,
    use_case: DeleteCourseUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle DELETE requests to remove a course.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the course to delete.
        use_case: Injected DeleteCourseUseCase.
        auth: Authenticated user context.
    """
    await use_case.execute(
        course_id=course_id,
        company_id=company_id,
        deleted_by=auth.user_id,
    )
