"""Admin list attempts route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import AdminListAttemptsUseCaseDependency
from ..mappers.attempt_mapper import AttemptMapper
from ..schemas.attempt_response_schema import AttemptResponseSchema


router = APIRouter()


@router.get(
    path="/{enrollment_id}/attempts/admin",
    status_code=status.HTTP_200_OK,
    summary="List all attempts for an enrollment (admin)",
)
async def handle_admin_list_attempts_route(
    company_id: str,
    enrollment_id: str,
    use_case: AdminListAttemptsUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> list[AttemptResponseSchema]:
    """Handle GET requests to list all attempts for any enrollment.

    Unlike the user-facing endpoint, this does not check enrollment
    ownership. Requires ADMIN role.

    Args:
        company_id: ULID of the company from the URL path.
        enrollment_id: ULID of the enrollment.
        use_case: Injected AdminListAttemptsUseCase.
        auth: Authenticated user context with ADMIN+ role.

    Returns:
        list[AttemptResponseSchema]: All attempts ordered by attempt_number.
    """
    entities = await use_case.execute(enrollment_id)
    return [AttemptMapper.to_response(e) for e in entities]
