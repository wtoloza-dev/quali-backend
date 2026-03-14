"""Reset attempts route handler."""

from typing import Annotated

from fastapi import APIRouter, Query, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import ResetAttemptsUseCaseDependency
from ..schemas.reset_attempts_response_schema import ResetAttemptsResponseSchema


router = APIRouter()


@router.delete(
    path="/{enrollment_id}/attempts",
    status_code=status.HTTP_200_OK,
    summary="Reset attempts for an enrollment (admin)",
)
async def handle_reset_attempts_route(
    company_id: str,
    enrollment_id: str,
    use_case: ResetAttemptsUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
    module_id: str | None = Query(default=None),
) -> ResetAttemptsResponseSchema:
    """Handle DELETE requests to reset attempts for an enrollment.

    When module_id is provided, only that module's attempts are deleted.
    When omitted, all attempts are deleted and status resets to not_started.
    Requires ADMIN role.

    Args:
        company_id: ULID of the company from the URL path.
        enrollment_id: ULID of the enrollment to reset.
        use_case: Injected ResetAttemptsUseCase.
        auth: Authenticated user context with ADMIN+ role.
        module_id: Optional ULID of the module to scope the reset.

    Returns:
        ResetAttemptsResponseSchema: The number of deleted attempts.
    """
    deleted_count = await use_case.execute(
        enrollment_id=enrollment_id,
        reset_by=auth.user_id,
        module_id=module_id,
    )
    return ResetAttemptsResponseSchema(deleted_count=deleted_count)
