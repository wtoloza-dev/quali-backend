"""Get course route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import OptionalCurrentUserDependency

from ...infrastructure.dependencies import GetCourseUseCaseDependency
from ..mappers.course_mapper import CourseMapper
from ..schemas.course_public_response_schema import CoursePublicResponseSchema
from ..schemas.course_response_schema import CourseResponseSchema


router = APIRouter()


@router.get(
    path="/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a course",
    description=(
        "Returns a course by ID. "
        "Private courses are only visible to the owning company. "
        "Authenticated users receive full data; unauthenticated users receive a public subset."
    ),
)
async def handle_get_course_route(
    company_id: str,
    course_id: str,
    use_case: GetCourseUseCaseDependency,
    auth: OptionalCurrentUserDependency,
) -> CourseResponseSchema | CoursePublicResponseSchema:
    """Handle GET requests to retrieve a single course.

    Args:
        company_id: ULID of the company resolved from the URL path.
        course_id: ULID of the course.
        use_case: Injected GetCourseUseCase.
        auth: Authenticated user context, or None if unauthenticated.

    Returns:
        Full course schema when authenticated, public schema otherwise.
    """
    course = await use_case.execute(course_id=course_id, company_id=company_id)
    if auth is not None:
        return CourseMapper.to_response(course)
    return CourseMapper.to_public_response(course)
