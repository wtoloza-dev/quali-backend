"""Archive course route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import ArchiveCourseUseCaseDependency
from ..mappers.course_mapper import CourseMapper
from ..schemas.course_response_schema import CourseResponseSchema


router = APIRouter()


@router.post(
    path="/{course_id}/archive",
    status_code=status.HTTP_200_OK,
    summary="Archive a course",
    description="Transitions a course to ARCHIVED status. Only the owning company can archive.",
)
async def handle_archive_course_route(
    company_id: str,
    course_id: str,
    use_case: ArchiveCourseUseCaseDependency,
    auth: CurrentUserDependency,
) -> CourseResponseSchema:
    """Handle POST requests to archive a course.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the course to archive.
        use_case: Injected ArchiveCourseUseCase.
        auth: Authenticated user context.

    Returns:
        CourseResponseSchema: The updated course with ARCHIVED status.
    """
    course = await use_case.execute(
        course_id=course_id,
        company_id=company_id,
        updated_by=auth.user_id,
    )
    return CourseMapper.to_response(course)
