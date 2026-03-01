"""List companies route handler."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListCompaniesUseCaseDependency
from ..mappers.company_mapper import CompanyMapper
from ..schemas import CompanyPublicResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List companies",
    description="Returns a paginated list of companies.",
)
async def handle_list_companies_route(
    pagination: Annotated[PaginationParams, Depends()],
    use_case: ListCompaniesUseCaseDependency,
    auth: CurrentUserDependency,
) -> PaginatedResponse[CompanyPublicResponseSchema]:
    """Handle GET requests to list companies with pagination.

    Args:
        pagination: Query parameters controlling page number and page size.
        use_case: Injected use case that fetches the paginated company data.
        auth: Authenticated user context.

    Returns:
        PaginatedResponse[CompanyPublicResponseSchema]: Paginated list of
        public company representations.
    """
    items, total = await use_case.execute(
        page=pagination.page,
        page_size=pagination.page_size,
    )
    return CompanyMapper.to_paginated_response(
        items=items, total=total, params=pagination
    )
