"""Update company member route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...domain.exceptions import CompanyMemberNotFoundException
from ...infrastructure.dependencies import (
    GetCompanyMemberMeUseCaseDependency,
    UpdateCompanyMemberUseCaseDependency,
)
from ..mappers.company_member_mapper import CompanyMemberMapper
from ..schemas.company_member_response_schema import CompanyMemberResponseSchema
from ..schemas.update_company_member_schema import UpdateCompanyMemberRequestSchema


router = APIRouter()


@router.patch(
    path="/{company_id}/members/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a company member's role",
    description="Updates the role of an existing company member. Requires ADMIN role.",
)
async def handle_update_company_member_route(
    company_id: str,
    user_id: str,
    body: Annotated[UpdateCompanyMemberRequestSchema, Body()],
    get_use_case: GetCompanyMemberMeUseCaseDependency,
    update_use_case: UpdateCompanyMemberUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> CompanyMemberResponseSchema:
    """Handle PATCH requests to update a company member's role.

    Fetches the existing membership, applies the role change, then
    delegates to UpdateCompanyMemberUseCase for persistence.

    Returns:
        CompanyMemberResponseSchema: The updated membership data.
    """
    existing = await get_use_case.execute(company_id, user_id)
    if not existing:
        raise CompanyMemberNotFoundException(
            user_id=user_id,
            company_id=company_id,
        )

    merged = existing.model_copy(update={"role": body.role, "updated_by": auth.user_id})
    member = await update_use_case.execute(merged)
    return CompanyMemberMapper.to_response(member)
