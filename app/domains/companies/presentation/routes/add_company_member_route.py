"""Add company member route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...domain.entities import CompanyMemberData
from ...infrastructure.dependencies import AddCompanyMemberUseCaseDependency
from ..mappers.company_member_mapper import CompanyMemberMapper
from ..schemas.add_company_member_schema import AddCompanyMemberRequestSchema
from ..schemas.company_member_response_schema import CompanyMemberResponseSchema


router = APIRouter()


@router.post(
    path="/{company_id}/members",
    status_code=status.HTTP_201_CREATED,
    summary="Add a user to a company",
    description="Adds a user as a member of a company. Fails if the user is already an active member.",
)
async def handle_add_company_member_route(
    company_id: str,
    body: Annotated[AddCompanyMemberRequestSchema, Body()],
    use_case: AddCompanyMemberUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> CompanyMemberResponseSchema:
    """Handle POST requests to add a user to a company.

    Returns:
        CompanyMemberResponseSchema: The newly created membership data.
    """
    data = CompanyMemberData(
        company_id=company_id, user_id=body.user_id, role=body.role
    )
    member = await use_case.execute(data, created_by=auth.user_id)
    return CompanyMemberMapper.to_response(member)
