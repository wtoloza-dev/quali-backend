"""Certificate token conflict exception."""

from app.shared.exceptions import ConflictException


class CertificateTokenConflictException(ConflictException):
    """Raised when a certificate integrity constraint is violated on save.

    Args:
        token: The verification token that caused the conflict.
    """

    def __init__(self, token: str) -> None:
        """Initialise the exception with the conflicting token.

        Args:
            token: The certificate verification token.
        """
        super().__init__(
            message=f"A certificate with token '{token}' already exists.",
            context={"token": token},
            error_code="CERTIFICATE_TOKEN_CONFLICT",
        )
