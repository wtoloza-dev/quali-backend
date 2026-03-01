"""Remove training plan item route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import RemoveTrainingPlanItemUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{plan_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a course item from a training plan",
)
async def handle_remove_training_plan_item_route(
    plan_id: str,  # noqa: ARG001 — URL context
    item_id: str,
    use_case: RemoveTrainingPlanItemUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> None:
    """Handle DELETE requests to remove an item from a training plan.

    Args:
        plan_id: ULID of the parent plan (URL context).
        item_id: ULID of the item to remove.
        use_case: Injected RemoveTrainingPlanItemUseCase.
        auth: Authenticated user context with ADMIN role.
    """
    await use_case.execute(item_id=item_id, deleted_by=auth.user_id)
