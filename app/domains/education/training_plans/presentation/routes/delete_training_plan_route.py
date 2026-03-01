"""Delete training plan route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import DeleteTrainingPlanUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a training plan",
)
async def handle_delete_training_plan_route(
    company_id: str,
    plan_id: str,
    use_case: DeleteTrainingPlanUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> None:
    """Handle DELETE requests to remove a training plan.

    Args:
        company_id: ULID of the company (from URL path).
        plan_id: ULID of the training plan to delete.
        use_case: Injected DeleteTrainingPlanUseCase.
        auth: Authenticated user context with ADMIN role.
    """
    await use_case.execute(
        plan_id=plan_id,
        company_id=company_id,
        deleted_by=auth.user_id,
    )
