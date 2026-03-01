"""Update enrollment status route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import UpdateEnrollmentStatusUseCaseDependency
from ..mappers.enrollment_mapper import EnrollmentMapper
from ..schemas.enrollment_response_schema import EnrollmentResponseSchema
from ..schemas.update_enrollment_status_schema import (
    UpdateEnrollmentStatusRequestSchema,
)


router = APIRouter()


@router.patch(
    path="/{enrollment_id}/status",
    status_code=status.HTTP_200_OK,
    summary="Update the status of an enrollment",
)
async def handle_update_enrollment_status_route(
    company_id: str,
    enrollment_id: str,
    body: UpdateEnrollmentStatusRequestSchema,
    use_case: UpdateEnrollmentStatusUseCaseDependency,
    auth: CurrentUserDependency,
) -> EnrollmentResponseSchema:
    """Handle PATCH requests to advance an enrollment's lifecycle status.

    Args:
        company_id: ULID of the owning company (from URL path).
        enrollment_id: ULID of the enrollment to update.
        body: New status value.
        use_case: Injected UpdateEnrollmentStatusUseCase.
        auth: Authenticated user context.

    Returns:
        EnrollmentResponseSchema: The updated enrollment.
    """
    entity = await use_case.execute(
        enrollment_id=enrollment_id,
        company_id=company_id,
        status=body.status,
        updated_by=auth.user_id,
    )
    return EnrollmentMapper.to_response(entity)
