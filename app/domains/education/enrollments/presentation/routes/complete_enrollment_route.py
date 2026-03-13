"""Complete enrollment route handler."""

from fastapi import APIRouter, status

from app.domains.certification.presentation.mappers import CertificateMapper
from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies.build_complete_enrollment_use_case_dependency import (
    CompleteEnrollmentUseCaseDependency,
)
from ..mappers.enrollment_mapper import EnrollmentMapper
from ..schemas.complete_enrollment_response_schema import (
    CompleteEnrollmentResponseSchema,
)


router = APIRouter()


@router.post(
    path="/{enrollment_id}/complete",
    status_code=status.HTTP_200_OK,
    summary="Complete an enrollment and issue a certificate",
)
async def handle_complete_enrollment_route(
    enrollment_id: str,
    use_case: CompleteEnrollmentUseCaseDependency,
    auth: CurrentUserDependency,
) -> CompleteEnrollmentResponseSchema:
    """Handle POST requests to complete an enrollment.

    Validates that all course modules have at least one passing attempt,
    marks the enrollment as completed, and issues a certificate.

    Args:
        enrollment_id: ULID of the enrollment to complete.
        use_case: Injected CompleteEnrollmentUseCase.
        auth: Authenticated user context.

    Returns:
        CompleteEnrollmentResponseSchema: Updated enrollment and new certificate.
    """
    enrollment, certificate = await use_case.execute(
        enrollment_id=enrollment_id,
        completed_by=auth.user_id,
    )
    return CompleteEnrollmentResponseSchema(
        enrollment=EnrollmentMapper.to_response(enrollment),
        certificate=CertificateMapper.to_private_response(certificate),
    )
