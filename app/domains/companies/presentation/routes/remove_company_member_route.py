"""Remove company member route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import RemoveCompanyMemberUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{company_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a member from a company",
    description="Permanently removes a company membership. A tombstone snapshot is archived for audit purposes.",
)
async def handle_remove_company_member_route(
    company_id: str,
    user_id: str,
    use_case: RemoveCompanyMemberUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> None:
    """Handle DELETE requests to remove a user from a company.

    Returns:
        None: 204 No Content on success.
    """
    await use_case.execute(
        company_id=company_id,
        user_id=user_id,
        deleted_by=auth.user_id,
    )
