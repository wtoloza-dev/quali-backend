"""List assessment attempts route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import ListAttemptsUseCaseDependency
from ..mappers.attempt_mapper import AttemptMapper
from ..schemas.attempt_response_schema import AttemptResponseSchema


router = APIRouter()


@router.get(
    path="/{enrollment_id}/attempts",
    status_code=status.HTTP_200_OK,
    summary="List all assessment attempts for an enrollment",
)
async def handle_list_attempts_route(
    enrollment_id: str,
    use_case: ListAttemptsUseCaseDependency,
    auth: CurrentUserDependency,  # noqa: ARG001 — auth guard
) -> list[AttemptResponseSchema]:
    """Handle GET requests to list all attempts for an enrollment.

    Args:
        enrollment_id: ULID of the enrollment (from URL path).
        use_case: Injected ListAttemptsUseCase.
        auth: Authenticated user context (required, not used directly).

    Returns:
        list[AttemptResponseSchema]: All attempts ordered by attempt_number.
    """
    entities = await use_case.execute(enrollment_id=enrollment_id)
    return [AttemptMapper.to_response(e) for e in entities]
