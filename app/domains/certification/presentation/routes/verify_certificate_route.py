"""Verify certificate route handler."""

from fastapi import APIRouter, status

from app.shared.contracts.get_user_by_id import GetUserByIdDependency

from ...infrastructure.dependencies import VerifyCertificateUseCaseDependency
from ..mappers.certificate_mapper import CertificateMapper
from ..schemas import CertificateVerifyResponseSchema


router = APIRouter()


@router.get(
    path="/verify/{token}",
    status_code=status.HTTP_200_OK,
    summary="Verify a certificate by QR token",
    description=(
        "Public endpoint. Verifies a certificate using the token embedded in its QR code. "
        "Returns the certificate status and public details for display on the verification page."
    ),
)
async def handle_verify_certificate_route(
    token: str,
    use_case: VerifyCertificateUseCaseDependency,
    get_user: GetUserByIdDependency,
) -> CertificateVerifyResponseSchema:
    """Handle GET requests to verify a certificate via its QR token.

    Args:
        token: The unique ULID token embedded in the QR code.
        use_case: Injected VerifyCertificateUseCase.
        get_user: Contract to look up the recipient's public data.

    Returns:
        CertificateVerifyResponseSchema: Public certificate data with computed status.
    """
    certificate = await use_case.execute(token=token)
    recipient = await get_user(user_id=certificate.recipient_id)
    return CertificateMapper.to_verify_response(certificate, recipient=recipient)
