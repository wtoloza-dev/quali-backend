"""Reorder modules route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import ReorderModulesUseCaseDependency
from ..schemas.reorder_schema import ReorderRequestSchema


router = APIRouter()


@router.put(
    path="/{course_id}/modules/order",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Reorder modules",
    description="Sets new order values for modules within a course.",
)
async def handle_reorder_modules_route(
    company_id: str,
    course_id: str,
    body: Annotated[ReorderRequestSchema, Body()],
    use_case: ReorderModulesUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle PUT requests to reorder modules.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the parent course.
        body: New order values for each module.
        use_case: Injected ReorderModulesUseCase.
        auth: Authenticated user context.
    """
    order_map = [(item.id, item.order) for item in body.items]
    await use_case.execute(
        course_id=course_id,
        company_id=company_id,
        order_map=order_map,
    )
