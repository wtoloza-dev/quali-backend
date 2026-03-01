"""List training plans route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListTrainingPlansUseCaseDependency
from ..mappers.training_plan_mapper import TrainingPlanMapper
from ..schemas.training_plan_response_schema import TrainingPlanResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List training plans for a company",
)
async def handle_list_training_plans_route(
    company_id: str,
    use_case: ListTrainingPlansUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],  # noqa: ARG001
    params: PaginationParams = PaginationParams(),
) -> PaginatedResponse[TrainingPlanResponseSchema]:
    """Handle GET requests to list all training plans for a company.

    Args:
        company_id: ULID of the company (from URL path).
        use_case: Injected ListTrainingPlansUseCase.
        auth: Authenticated user context with VIEWER role.
        params: Pagination parameters.

    Returns:
        PaginatedResponse[TrainingPlanResponseSchema]: Paginated plan list.
    """
    items, total = await use_case.execute(company_id=company_id, params=params)
    return TrainingPlanMapper.to_paginated_response(items, total, params)
