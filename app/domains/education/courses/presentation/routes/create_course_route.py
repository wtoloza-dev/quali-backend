"""Create course route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.entities import CourseData
from ...domain.enums import CourseStatus
from ...infrastructure.dependencies import CreateCourseUseCaseDependency
from ..mappers.course_mapper import CourseMapper
from ..schemas.course_response_schema import CourseResponseSchema
from ..schemas.create_course_schema import CreateCourseRequestSchema


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a course",
    description="Creates a new course in DRAFT status for the authenticated company.",
)
async def handle_create_course_route(
    company_id: str,
    body: Annotated[CreateCourseRequestSchema, Body()],
    use_case: CreateCourseUseCaseDependency,
    auth: CurrentUserDependency,
) -> CourseResponseSchema:
    """Handle POST requests to create a course.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        body: Validated course creation request.
        use_case: Injected CreateCourseUseCase.
        auth: Authenticated user context.

    Returns:
        CourseResponseSchema: The newly created course.
    """
    course = await use_case.execute(
        data=CourseData(
            company_id=company_id,
            title=body.title,
            description=body.description,
            vertical=body.vertical,
            regulatory_ref=body.regulatory_ref,
            validity_days=body.validity_days,
            visibility=body.visibility,
            status=CourseStatus.DRAFT,
        ),
        created_by=auth.user_id,
    )
    return CourseMapper.to_response(course)
