"""Publish course route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import PublishCourseUseCaseDependency
from ..mappers.course_mapper import CourseMapper
from ..schemas.course_response_schema import CourseResponseSchema


router = APIRouter()


@router.post(
    path="/{course_id}/publish",
    status_code=status.HTTP_200_OK,
    summary="Publish a course",
    description="Transitions a course from DRAFT to PUBLISHED. Only the owning company can publish.",
)
async def handle_publish_course_route(
    company_id: str,
    course_id: str,
    use_case: PublishCourseUseCaseDependency,
    auth: CurrentUserDependency,
) -> CourseResponseSchema:
    """Handle POST requests to publish a course.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the course to publish.
        use_case: Injected PublishCourseUseCase.
        auth: Authenticated user context.

    Returns:
        CourseResponseSchema: The updated course with PUBLISHED status.
    """
    course = await use_case.execute(
        course_id=course_id,
        company_id=company_id,
        updated_by=auth.user_id,
    )
    return CourseMapper.to_response(course)
