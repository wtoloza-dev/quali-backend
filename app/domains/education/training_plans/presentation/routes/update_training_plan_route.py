"""Update training plan route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import (
    GetTrainingPlanUseCaseDependency,
    UpdateTrainingPlanUseCaseDependency,
)
from ..mappers.training_plan_mapper import TrainingPlanMapper
from ..schemas.training_plan_response_schema import TrainingPlanResponseSchema
from ..schemas.update_training_plan_schema import UpdateTrainingPlanRequestSchema


router = APIRouter()


@router.patch(
    path="/{plan_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a training plan",
)
async def handle_update_training_plan_route(
    company_id: str,
    plan_id: str,
    body: UpdateTrainingPlanRequestSchema,
    get_use_case: GetTrainingPlanUseCaseDependency,
    update_use_case: UpdateTrainingPlanUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.MEMBER)],
) -> TrainingPlanResponseSchema:
    """Handle PATCH requests to update a training plan.

    Args:
        company_id: ULID of the company (from URL path).
        plan_id: ULID of the training plan to update.
        body: Fields to update (title, status).
        get_use_case: Injected GetTrainingPlanUseCase.
        update_use_case: Injected UpdateTrainingPlanUseCase.
        auth: Authenticated user context with MEMBER role.

    Returns:
        TrainingPlanResponseSchema: The updated plan.
    """
    entity = await get_use_case.execute(plan_id=plan_id, company_id=company_id)
    updated = entity.model_copy(
        update={
            k: v
            for k, v in {
                "title": body.title,
                "status": body.status,
                "updated_by": auth.user_id,
            }.items()
            if v is not None
        }
    )
    result = await update_use_case.execute(entity=updated)
    return TrainingPlanMapper.to_response(result)
