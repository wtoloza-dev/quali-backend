"""List certificates route handler."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListCertificatesUseCaseDependency
from ..mappers.certificate_mapper import CertificateMapper
from ..schemas import CertificatePrivateResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List certificates for a company",
    description="Returns a paginated list of certificates issued by the company. Requires at least VIEWER role.",
)
async def handle_list_certificates_route(
    company_id: str,
    pagination: Annotated[PaginationParams, Depends()],
    use_case: ListCertificatesUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],
) -> PaginatedResponse[CertificatePrivateResponseSchema]:
    """Handle GET requests to list certificates for a company.

    Args:
        company_id: ULID of the company, resolved from the URL path.
        pagination: Parsed page and page_size query parameters.
        use_case: Injected ListCertificatesUseCase.
        auth: Authenticated user context with at least VIEWER role.

    Returns:
        PaginatedResponse[CertificatePrivateResponseSchema]: Paginated certificate list.
    """
    items, total = await use_case.execute(
        company_id=company_id,
        page=pagination.page,
        page_size=pagination.page_size,
    )
    return CertificateMapper.to_paginated_response(items, total, pagination)
