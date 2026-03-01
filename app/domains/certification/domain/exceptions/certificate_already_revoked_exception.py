"""Certificate already revoked exception."""

from app.shared.exceptions import ConflictException


class CertificateAlreadyRevokedException(ConflictException):
    """Raised when attempting to revoke a certificate that is already revoked.

    Args:
        certificate_id: The ULID of the already-revoked certificate.
    """

    def __init__(self, certificate_id: str) -> None:
        """Initialise the exception with the affected certificate identifier.

        Args:
            certificate_id: The ULID of the already-revoked certificate.
        """
        super().__init__(
            message=f"Certificate '{certificate_id}' has already been revoked.",
            context={"certificate_id": certificate_id},
            error_code="CERTIFICATE_ALREADY_REVOKED",
        )
