"""Get company members route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role
from app.shared.contracts import GetUserByIdDependency

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
    get_user: GetUserByIdDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],
) -> list[CompanyMemberResponseSchema]:
    """Handle GET requests to list all active members of a company.

    Enriches each member with user info (email, first_name, last_name)
    via the get_user_by_id contract.

    Returns:
        list[CompanyMemberResponseSchema]: All active memberships with user info.
    """
    members = await use_case.execute(company_id)

    user_ids = {m.user_id for m in members}
    user_map = {}
    for uid in user_ids:
        user = await get_user(user_id=uid)
        if user:
            user_map[uid] = user

    result = []
    for member in members:
        schema = CompanyMemberMapper.to_response(member)
        user = user_map.get(member.user_id)
        if user:
            schema.email = user.email
            schema.first_name = user.first_name
            schema.last_name = user.last_name
        result.append(schema)

    return result
