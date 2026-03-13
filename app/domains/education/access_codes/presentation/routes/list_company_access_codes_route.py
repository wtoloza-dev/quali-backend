"""List company access codes route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListCompanyAccessCodesUseCaseDependency
from ..mappers.access_code_mapper import AccessCodeMapper
from ..schemas.access_code_response_schema import AccessCodeResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List all access codes for a company",
)
async def handle_list_company_access_codes_route(
    company_id: str,
    use_case: ListCompanyAccessCodesUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
    params: PaginationParams = PaginationParams(),
) -> PaginatedResponse[AccessCodeResponseSchema]:
    """Handle GET requests to list all access codes for a company.

    Requires ADMIN role or superadmin access.

    Args:
        company_id: ULID of the company from the URL path.
        use_case: Injected ListCompanyAccessCodesUseCase.
        auth: Authenticated user context with ADMIN+ role.
        params: Pagination parameters.

    Returns:
        PaginatedResponse[AccessCodeResponseSchema]: Paginated access code list.
    """
    items, total = await use_case.execute(
        company_id=company_id,
        params=params,
    )
    return AccessCodeMapper.to_paginated_response(items, total, params)
