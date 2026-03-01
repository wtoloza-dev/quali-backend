"""Check course access route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import CheckCourseAccessUseCaseDependency


router = APIRouter()


@router.get(
    path="/{course_id}/access",
    status_code=status.HTTP_200_OK,
    summary="Check if the current user has full course access",
)
async def handle_check_course_access_route(
    course_id: str,
    use_case: CheckCourseAccessUseCaseDependency,
    auth: CurrentUserDependency,
) -> dict:
    """Handle GET requests to check course access for the authenticated user.

    Args:
        course_id: ULID of the course.
        use_case: Injected CheckCourseAccessUseCase.
        auth: Authenticated user context.

    Returns:
        dict: {"has_access": bool}
    """
    has_access = await use_case.execute(
        user_id=auth.user_id,
        course_id=course_id,
    )
    return {"has_access": has_access}
