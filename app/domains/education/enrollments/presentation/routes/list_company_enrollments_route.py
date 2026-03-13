"""List company enrollments route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListCompanyEnrollmentsUseCaseDependency
from ..mappers.enrollment_mapper import EnrollmentMapper
from ..schemas.enrollment_response_schema import EnrollmentResponseSchema


router = APIRouter()


@router.get(
    path="/all",
    status_code=status.HTTP_200_OK,
    summary="List all enrollments for a company",
)
async def handle_list_company_enrollments_route(
    company_id: str,
    use_case: ListCompanyEnrollmentsUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
    params: PaginationParams = PaginationParams(),
) -> PaginatedResponse[EnrollmentResponseSchema]:
    """Handle GET requests to list all enrollments for a company.

    Requires ADMIN role or superadmin access.

    Args:
        company_id: ULID of the company from the URL path.
        use_case: Injected ListCompanyEnrollmentsUseCase.
        auth: Authenticated user context with ADMIN+ role.
        params: Pagination parameters.

    Returns:
        PaginatedResponse[EnrollmentResponseSchema]: Paginated enrollment list.
    """
    items, total = await use_case.execute(
        company_id=company_id,
        params=params,
    )
    return EnrollmentMapper.to_paginated_response(items, total, params)
