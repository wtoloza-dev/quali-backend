"""Certificate not found exception."""

from app.shared.exceptions import NotFoundException


class CertificateNotFoundException(NotFoundException):
    """Raised when a certificate cannot be found by ID or token.

    Args:
        certificate_id: The identifier that was not found.
    """

    def __init__(self, certificate_id: str) -> None:
        """Initialise the exception with the missing certificate identifier.

        Args:
            certificate_id: The ULID or token that produced no result.
        """
        super().__init__(
            message=f"Certificate '{certificate_id}' not found.",
            context={"certificate_id": certificate_id},
            error_code="CERTIFICATE_NOT_FOUND",
        )
