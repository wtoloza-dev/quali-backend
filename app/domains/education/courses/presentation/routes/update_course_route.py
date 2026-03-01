"""Update course route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.exceptions import CourseNotFoundException
from ...infrastructure.dependencies import (
    GetCourseUseCaseDependency,
    UpdateCourseUseCaseDependency,
)
from ..mappers.course_mapper import CourseMapper
from ..schemas.course_response_schema import CourseResponseSchema
from ..schemas.update_course_schema import UpdateCourseRequestSchema


router = APIRouter()


@router.patch(
    path="/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a course",
    description="Partially updates a course. Only the owning company can update.",
)
async def handle_update_course_route(
    company_id: str,
    course_id: str,
    body: Annotated[UpdateCourseRequestSchema, Body()],
    get_use_case: GetCourseUseCaseDependency,
    update_use_case: UpdateCourseUseCaseDependency,
    auth: CurrentUserDependency,
) -> CourseResponseSchema:
    """Handle PATCH requests to update a course.

    Fetches the existing course, merges provided fields, and persists.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the course to update.
        body: Fields to update.
        get_use_case: Injected GetCourseUseCase.
        update_use_case: Injected UpdateCourseUseCase.
        auth: Authenticated user context.

    Returns:
        CourseResponseSchema: The updated course.
    """
    existing = await get_use_case.execute(course_id=course_id, company_id=company_id)

    if existing.company_id != company_id:
        raise CourseNotFoundException(course_id=course_id)

    patch = body.model_dump(exclude_none=True)
    merged = existing.model_copy(update=patch)

    updated = await update_use_case.execute(entity=merged, updated_by=auth.user_id)
    return CourseMapper.to_response(updated)
