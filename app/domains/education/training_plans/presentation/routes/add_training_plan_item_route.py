"""Add training plan item route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...domain.entities import TrainingPlanItemData
from ...infrastructure.dependencies import AddTrainingPlanItemUseCaseDependency
from ..mappers.training_plan_mapper import TrainingPlanMapper
from ..schemas.add_training_plan_item_schema import AddTrainingPlanItemRequestSchema
from ..schemas.training_plan_item_response_schema import (
    TrainingPlanItemResponseSchema,
)


router = APIRouter()


@router.post(
    path="/{plan_id}/items",
    status_code=status.HTTP_201_CREATED,
    summary="Add a course item to a training plan",
)
async def handle_add_training_plan_item_route(
    plan_id: str,
    body: AddTrainingPlanItemRequestSchema,
    use_case: AddTrainingPlanItemUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.MEMBER)],
) -> TrainingPlanItemResponseSchema:
    """Handle POST requests to add a course to a training plan.

    Args:
        plan_id: ULID of the training plan (from URL path).
        body: Item data including course_id and optional targeting.
        use_case: Injected AddTrainingPlanItemUseCase.
        auth: Authenticated user context with MEMBER role.

    Returns:
        TrainingPlanItemResponseSchema: The created item.
    """
    data = TrainingPlanItemData(
        plan_id=plan_id,
        course_id=body.course_id,
        target_role=body.target_role,
        scheduled_date=body.scheduled_date,
        notes=body.notes,
    )
    entity = await use_case.execute(data=data, created_by=auth.user_id)
    return TrainingPlanMapper.item_to_response(entity)
