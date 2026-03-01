"""Create training plan route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...domain.entities import TrainingPlanData
from ...infrastructure.dependencies import CreateTrainingPlanUseCaseDependency
from ..mappers.training_plan_mapper import TrainingPlanMapper
from ..schemas.create_training_plan_schema import CreateTrainingPlanRequestSchema
from ..schemas.training_plan_response_schema import TrainingPlanResponseSchema


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create an annual training plan",
)
async def handle_create_training_plan_route(
    company_id: str,
    body: CreateTrainingPlanRequestSchema,
    use_case: CreateTrainingPlanUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.MEMBER)],
) -> TrainingPlanResponseSchema:
    """Handle POST requests to create a training plan.

    Args:
        company_id: ULID of the company (from URL path).
        body: Plan data including year and title.
        use_case: Injected CreateTrainingPlanUseCase.
        auth: Authenticated user context with MEMBER role.

    Returns:
        TrainingPlanResponseSchema: The created training plan.
    """
    data = TrainingPlanData(
        company_id=company_id,
        year=body.year,
        title=body.title,
    )
    entity = await use_case.execute(data=data, created_by=auth.user_id)
    return TrainingPlanMapper.to_response(entity)
