"""Delete company route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import DeleteCompanyUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a company",
    description="Permanently deletes a company. A tombstone snapshot is archived for audit purposes.",
)
async def handle_delete_company_route(
    company_id: str,
    use_case: DeleteCompanyUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.OWNER)],
) -> None:
    """Handle DELETE requests to permanently delete a company."""
    await use_case.execute(company_id=company_id, deleted_by=auth.user_id)
