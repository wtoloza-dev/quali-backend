"""Issue certificate route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...domain.entities import CertificateData
from ...infrastructure.dependencies import IssueCertificateUseCaseDependency
from ..mappers.certificate_mapper import CertificateMapper
from ..schemas import CertificatePrivateResponseSchema, IssueCertificateRequestSchema


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Issue a new digital certificate",
    description="Issues a new digital certificate to the specified recipient. Requires at least MEMBER role in the company.",
)
async def handle_issue_certificate_route(
    company_id: str,
    body: Annotated[IssueCertificateRequestSchema, Body()],
    use_case: IssueCertificateUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.MEMBER)],
) -> CertificatePrivateResponseSchema:
    """Handle POST requests to issue a new digital certificate.

    Args:
        company_id: ULID of the issuing company, resolved from the URL path.
        body: Validated issue certificate request body.
        use_case: Injected IssueCertificateUseCase.
        auth: Authenticated user context with at least MEMBER role.

    Returns:
        CertificatePrivateResponseSchema: The newly issued certificate data.
    """
    data = CertificateData(
        company_id=company_id,
        recipient_id=body.recipient_id,
        title=body.title,
        description=body.description,
        issued_at=body.issued_at,
        expires_at=body.expires_at,
    )
    certificate = await use_case.execute(data, created_by=auth.user_id)
    return CertificateMapper.to_private_response(certificate)
