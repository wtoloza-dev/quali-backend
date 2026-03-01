"""Get training plan route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import GetTrainingPlanUseCaseDependency
from ..mappers.training_plan_mapper import TrainingPlanMapper
from ..schemas.training_plan_response_schema import TrainingPlanResponseSchema


router = APIRouter()


@router.get(
    path="/{plan_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a training plan by ID",
)
async def handle_get_training_plan_route(
    company_id: str,
    plan_id: str,
    use_case: GetTrainingPlanUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],  # noqa: ARG001
) -> TrainingPlanResponseSchema:
    """Handle GET requests to retrieve a single training plan.

    Args:
        company_id: ULID of the company (from URL path).
        plan_id: ULID of the training plan.
        use_case: Injected GetTrainingPlanUseCase.
        auth: Authenticated user context with VIEWER role.

    Returns:
        TrainingPlanResponseSchema: The matching plan.
    """
    entity = await use_case.execute(plan_id=plan_id, company_id=company_id)
    return TrainingPlanMapper.to_response(entity)
