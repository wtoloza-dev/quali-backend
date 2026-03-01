"""Unenroll route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import UnenrollUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove an enrollment",
)
async def handle_unenroll_route(
    company_id: str,
    enrollment_id: str,
    use_case: UnenrollUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle DELETE requests to remove an enrollment.

    Args:
        company_id: ULID of the owning company (from URL path).
        enrollment_id: ULID of the enrollment to remove.
        use_case: Injected UnenrollUseCase.
        auth: Authenticated user context.
    """
    await use_case.execute(
        enrollment_id=enrollment_id,
        company_id=company_id,
        deleted_by=auth.user_id,
    )
