"""Get company members route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import GetCompanyMembersUseCaseDependency
from ..mappers.company_member_mapper import CompanyMemberMapper
from ..schemas.company_member_response_schema import CompanyMemberResponseSchema


router = APIRouter()


@router.get(
    path="/{company_id}/members",
    status_code=status.HTTP_200_OK,
    summary="List company members",
    description="Returns all active members of a company.",
)
async def handle_get_company_members_route(
    company_id: str,
    use_case: GetCompanyMembersUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],
) -> list[CompanyMemberResponseSchema]:
    """Handle GET requests to list all active members of a company.

    Returns:
        list[CompanyMemberResponseSchema]: All active memberships for the company.
    """
    members = await use_case.execute(company_id)
    return [CompanyMemberMapper.to_response(m) for m in members]
