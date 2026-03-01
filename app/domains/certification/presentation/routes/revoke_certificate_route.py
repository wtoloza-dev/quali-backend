"""Revoke certificate route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role

from ...infrastructure.dependencies import RevokeCertificateUseCaseDependency
from ..mappers.certificate_mapper import CertificateMapper
from ..schemas import CertificatePrivateResponseSchema, RevokeCertificateRequestSchema


router = APIRouter()


@router.patch(
    path="/{certificate_id}/revoke",
    status_code=status.HTTP_200_OK,
    summary="Revoke a certificate",
    description="Revokes an active certificate. A mandatory reason must be provided. Requires at least ADMIN role.",
)
async def handle_revoke_certificate_route(
    company_id: str,
    certificate_id: str,
    body: Annotated[RevokeCertificateRequestSchema, Body()],
    use_case: RevokeCertificateUseCaseDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
) -> CertificatePrivateResponseSchema:
    """Handle PATCH requests to revoke a certificate.

    Args:
        company_id: ULID of the company, resolved from the URL path.
        certificate_id: The ULID of the certificate to revoke.
        body: Validated revoke request body with reason.
        use_case: Injected RevokeCertificateUseCase.
        auth: Authenticated user context with at least ADMIN role.

    Returns:
        CertificatePrivateResponseSchema: The updated certificate with REVOKED status.
    """
    certificate = await use_case.execute(
        certificate_id=certificate_id,
        company_id=company_id,
        revoked_by=auth.user_id,
        reason=body.reason,
    )
    return CertificateMapper.to_private_response(certificate)
