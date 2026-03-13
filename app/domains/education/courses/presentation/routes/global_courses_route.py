"""Global course routes for superadmin access.

These endpoints are not company-scoped. They return data across all
companies and require the requesting user to be a superadmin.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.contracts import GetUserByIdDependency
from app.shared.exceptions import InsufficientPermissionsException
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import (
    ListAllCoursesUseCaseDependency,
    ListLessonsUseCaseDependency,
    ListModulesUseCaseDependency,
)
from ..mappers.course_mapper import CourseMapper
from ..mappers.module_mapper import ModuleMapper
from ..schemas.course_response_schema import CourseResponseSchema
from ..schemas.lesson_summary_schema import LessonSummaryResponseSchema
from ..schemas.module_response_schema import ModuleResponseSchema


router = APIRouter()


async def _require_superadmin(
    auth: CurrentUserDependency,
    get_user: GetUserByIdDependency,
) -> None:
    """Verify the current user is a superadmin.

    Args:
        auth: Authenticated user context.
        get_user: Contract adapter to look up user details.

    Raises:
        InsufficientPermissionsException: If the user is not a superadmin.
    """
    user = await get_user(user_id=auth.user_id)
    if not user or not user.is_superadmin:
        raise InsufficientPermissionsException(
            required_role="superadmin",
            company_id="global",
        )


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List all courses (superadmin)",
    description=(
        "Returns a paginated list of all courses across all companies. Superadmin only."
    ),
)
async def handle_list_all_courses_route(
    pagination: Annotated[PaginationParams, Depends()],
    use_case: ListAllCoursesUseCaseDependency,
    auth: CurrentUserDependency,
    get_user: GetUserByIdDependency,
) -> PaginatedResponse[CourseResponseSchema]:
    """Handle GET requests to list all courses globally.

    Args:
        pagination: Query parameters controlling page number and page size.
        use_case: Injected ListAllCoursesUseCase.
        auth: Authenticated user context.
        get_user: Contract adapter to look up user details.

    Returns:
        Paginated list of all courses.
    """
    await _require_superadmin(auth, get_user)

    items, total = await use_case.execute(
        page=pagination.page,
        page_size=pagination.page_size,
    )
    return CourseMapper.to_paginated_response(
        items=items,
        total=total,
        params=pagination,
        authenticated=True,
    )


@router.get(
    path="/{course_id}/modules",
    status_code=status.HTTP_200_OK,
    summary="List modules for a course (superadmin)",
    description=("Returns all modules for a given course. Superadmin only."),
)
async def handle_list_all_course_modules_route(
    course_id: str,
    use_case: ListModulesUseCaseDependency,
    auth: CurrentUserDependency,
    get_user: GetUserByIdDependency,
) -> list[ModuleResponseSchema]:
    """Handle GET requests to list modules for a course globally.

    Args:
        course_id: ULID of the course.
        use_case: Injected ListModulesUseCase.
        auth: Authenticated user context.
        get_user: Contract adapter to look up user details.

    Returns:
        List of modules for the course.
    """
    await _require_superadmin(auth, get_user)
    items = await use_case.execute(course_id=course_id)
    return [ModuleMapper.to_response(m) for m in items]


@router.get(
    path="/{course_id}/modules/{module_id}/lessons",
    status_code=status.HTTP_200_OK,
    summary="List lessons for a module (superadmin)",
    description=("Returns all lessons for a given module. Superadmin only."),
)
async def handle_list_all_module_lessons_route(
    course_id: str,
    module_id: str,
    use_case: ListLessonsUseCaseDependency,
    auth: CurrentUserDependency,
    get_user: GetUserByIdDependency,
) -> list[LessonSummaryResponseSchema]:
    """Handle GET requests to list lessons for a module globally.

    Args:
        course_id: ULID of the parent course.
        module_id: ULID of the module.
        use_case: Injected ListLessonsUseCase.
        auth: Authenticated user context.
        get_user: Contract adapter to look up user details.

    Returns:
        List of lesson summaries for the module.
    """
    await _require_superadmin(auth, get_user)
    items = await use_case.execute(module_id=module_id)
    return [
        LessonSummaryResponseSchema(
            id=lesson.id,
            module_id=lesson.module_id,
            title=lesson.title,
            is_preview=lesson.is_preview,
            order=lesson.order,
            created_at=lesson.created_at,
        )
        for lesson in items
    ]
