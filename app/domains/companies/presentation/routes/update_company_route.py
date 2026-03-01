"""Update company route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...domain.value_objects import Tax  # noqa: F401 — used for Tax coercion in patch
from ...infrastructure.dependencies import (
    GetCompanyUseCaseDependency,
    UpdateCompanyUseCaseDependency,
)
from ..mappers.company_mapper import CompanyMapper
from ..schemas import CompanyPrivateResponseSchema, UpdateCompanyRequestSchema


router = APIRouter()


@router.patch(
    path="/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a company",
    description="Applies partial updates to an existing company. Only accessible to authenticated company members.",
)
async def handle_update_company_route(
    company_id: str,
    body: Annotated[UpdateCompanyRequestSchema, Body()],
    get_use_case: GetCompanyUseCaseDependency,
    update_use_case: UpdateCompanyUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> CompanyPrivateResponseSchema:
    """Handle PATCH requests to update a company.

    Fetches the existing entity, applies only the non-None fields from
    the request body, then delegates to UpdateCompanyUseCase for
    business rule validation and persistence.

    Returns:
        CompanyPrivateResponseSchema: Updated company data.
    """
    existing = await get_use_case.execute(company_id)

    patch = body.model_dump(exclude_none=True)
    if "tax" in patch and body.tax is not None:
        patch["tax"] = Tax(tax_type=body.tax.tax_type, tax_id=body.tax.tax_id)

    merged = existing.model_copy(update=patch)
    company = await update_use_case.execute(merged)
    return CompanyMapper.to_private_response(company)
