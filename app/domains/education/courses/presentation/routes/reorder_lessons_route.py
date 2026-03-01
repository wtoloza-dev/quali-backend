"""Reorder lessons route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import ReorderLessonsUseCaseDependency
from ..schemas.reorder_schema import ReorderRequestSchema


router = APIRouter()


@router.put(
    path="/{course_id}/modules/{module_id}/lessons/order",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Reorder lessons",
    description="Sets new order values for lessons within a module.",
)
async def handle_reorder_lessons_route(
    company_id: str,
    course_id: str,
    module_id: str,
    body: Annotated[ReorderRequestSchema, Body()],
    use_case: ReorderLessonsUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle PUT requests to reorder lessons.

    Args:
        company_id: ULID of the owning company from the URL path.
        course_id: ULID of the parent course.
        module_id: ULID of the parent module.
        body: New order values for each lesson.
        use_case: Injected ReorderLessonsUseCase.
        auth: Authenticated user context.
    """
    order_map = [(item.id, item.order) for item in body.items]
    await use_case.execute(
        course_id=course_id,
        company_id=company_id,
        module_id=module_id,
        order_map=order_map,
    )
