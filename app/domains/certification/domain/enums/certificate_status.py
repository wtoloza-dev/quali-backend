"""Certificate status enum."""

from enum import StrEnum


class CertificateStatus(StrEnum):
    """Lifecycle states of a digital certificate.

    Attributes:
        ACTIVE: Certificate is valid and has not been revoked or expired.
        REVOKED: Certificate was explicitly revoked before its expiration.
        EXPIRED: Certificate passed its expiration date without being revoked.
    """

    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
