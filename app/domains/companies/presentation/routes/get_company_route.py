"""Get company route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import GetCompanyUseCaseDependency
from ..mappers.company_mapper import CompanyMapper
from ..schemas import CompanyPrivateResponseSchema


router = APIRouter()


@router.get(
    path="/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a company by ID",
    description="Retrieves full company details. Only accessible to authenticated company members.",
)
async def handle_get_company_route(
    company_id: str,
    use_case: GetCompanyUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],
) -> CompanyPrivateResponseSchema:
    """Handle GET requests to retrieve a company by its ULID.

    Returns:
        CompanyPrivateResponseSchema: Full company data for authenticated members.
    """
    company = await use_case.execute(company_id)
    return CompanyMapper.to_private_response(company)
