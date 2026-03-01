"""Get certificate route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import GetCertificateUseCaseDependency
from ..mappers.certificate_mapper import CertificateMapper
from ..schemas import CertificatePrivateResponseSchema


router = APIRouter()


@router.get(
    path="/{certificate_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a certificate by ID",
    description="Retrieves a single certificate by its ULID. Requires at least VIEWER role in the company.",
)
async def handle_get_certificate_route(
    company_id: str,
    certificate_id: str,
    use_case: GetCertificateUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],
) -> CertificatePrivateResponseSchema:
    """Handle GET requests to retrieve a certificate by its ULID.

    Args:
        company_id: ULID of the company, resolved from the URL path.
        certificate_id: The ULID of the certificate to retrieve.
        use_case: Injected GetCertificateUseCase.
        auth: Authenticated user context with at least VIEWER role.

    Returns:
        CertificatePrivateResponseSchema: The found certificate data.
    """
    certificate = await use_case.execute(
        certificate_id=certificate_id, company_id=company_id
    )
    return CertificateMapper.to_private_response(certificate)
