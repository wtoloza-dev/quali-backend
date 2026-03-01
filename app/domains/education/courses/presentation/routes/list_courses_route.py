"""List courses route handler."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.shared.auth.dependencies import OptionalCurrentUserDependency
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListCoursesUseCaseDependency
from ..mappers.course_mapper import CourseMapper
from ..schemas.course_public_response_schema import CoursePublicResponseSchema
from ..schemas.course_response_schema import CourseResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List courses",
    description=(
        "Returns a paginated list of courses visible to the company. "
        "Authenticated users receive full course data. "
        "Unauthenticated users receive a public subset (no company internals)."
    ),
)
async def handle_list_courses_route(
    company_id: str,
    pagination: Annotated[PaginationParams, Depends()],
    use_case: ListCoursesUseCaseDependency,
    auth: OptionalCurrentUserDependency,
) -> PaginatedResponse[CourseResponseSchema | CoursePublicResponseSchema]:
    """Handle GET requests to list courses.

    Args:
        company_id: ULID of the company resolved from the URL path.
        pagination: Query parameters controlling page number and page size.
        use_case: Injected ListCoursesUseCase.
        auth: Authenticated user context, or None if unauthenticated.

    Returns:
        Paginated list of courses. Full schema when authenticated, public schema otherwise.
    """
    items, total = await use_case.execute(
        page=pagination.page,
        page_size=pagination.page_size,
        company_id=company_id,
    )
    return CourseMapper.to_paginated_response(
        items=items,
        total=total,
        params=pagination,
        authenticated=auth is not None,
    )
