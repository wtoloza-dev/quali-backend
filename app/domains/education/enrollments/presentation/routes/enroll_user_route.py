"""Enroll user route handler."""

from fastapi import APIRouter, Request, status

from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.contracts.save_legal_acceptance import (
    LegalAcceptanceContractInput,
    SaveLegalAcceptanceDependency,
)
from app.shared.exceptions import UnprocessableException

from ...domain.entities import EnrollmentData
from ...infrastructure.dependencies import EnrollUserUseCaseDependency
from ..mappers.enrollment_mapper import EnrollmentMapper
from ..schemas.enroll_user_schema import EnrollUserRequestSchema
from ..schemas.enrollment_response_schema import EnrollmentResponseSchema


ENROLLMENT_DECLARATION = (
    "Declaro que soy la persona identificada en mi perfil y que realizaré "
    "personalmente todas las actividades de este curso. Entiendo que la "
    "certificación obtenida es intransferible y que cualquier suplantación "
    "o fraude invalida el certificado emitido."
)

router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Enroll a user in a course",
)
async def handle_enroll_user_route(
    company_id: str,
    body: EnrollUserRequestSchema,
    request: Request,
    use_case: EnrollUserUseCaseDependency,
    save_legal_acceptance: SaveLegalAcceptanceDependency,
    auth: CurrentUserDependency,
) -> EnrollmentResponseSchema:
    """Handle POST requests to enroll a user in a course.

    Args:
        company_id: ULID of the company (from URL path).
        body: Enrollment request data.
        request: FastAPI request (for client IP).
        use_case: Injected EnrollUserUseCase.
        save_legal_acceptance: Contract adapter to persist legal acceptance records.
        auth: Authenticated user context.

    Returns:
        EnrollmentResponseSchema: The created enrollment.
    """
    if not body.legal_accepted:
        raise UnprocessableException(
            message="Debes aceptar la declaración legal para inscribirte.",
            error_code="LEGAL_NOT_ACCEPTED",
        )

    data = EnrollmentData(
        user_id=auth.user_id,
        course_id=body.course_id,
        company_id=company_id,
        is_mandatory=body.is_mandatory,
    )
    entity = await use_case.execute(data=data, created_by=auth.user_id)

    # Record the legal acceptance tied to this enrollment.
    client_ip = request.client.host if request.client else None
    await save_legal_acceptance(
        LegalAcceptanceContractInput(
            user_id=auth.user_id,
            enrollment_id=entity.id,
            acceptance_type="enrollment_identity",
            declaration_text=ENROLLMENT_DECLARATION,
            ip_address=client_ip,
        )
    )

    return EnrollmentMapper.to_response(entity)
