"""Get enrollment route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import GetEnrollmentUseCaseDependency
from ..mappers.enrollment_mapper import EnrollmentMapper
from ..schemas.enrollment_response_schema import EnrollmentResponseSchema


router = APIRouter()


@router.get(
    path="/{enrollment_id}",
    status_code=status.HTTP_200_OK,
    summary="Get an enrollment by ID",
)
async def handle_get_enrollment_route(
    company_id: str,
    enrollment_id: str,
    use_case: GetEnrollmentUseCaseDependency,
    auth: CurrentUserDependency,  # noqa: ARG001 — auth guard
) -> EnrollmentResponseSchema:
    """Handle GET requests to retrieve a single enrollment.

    Args:
        company_id: ULID of the owning company (from URL path).
        enrollment_id: ULID of the enrollment to retrieve.
        use_case: Injected GetEnrollmentUseCase.
        auth: Authenticated user context (required, not used directly).

    Returns:
        EnrollmentResponseSchema: The matching enrollment.
    """
    entity = await use_case.execute(enrollment_id=enrollment_id, company_id=company_id)
    return EnrollmentMapper.to_response(entity)
