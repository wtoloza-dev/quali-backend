"""Certificate revoked domain event."""

from pydantic import BaseModel


class CertificateRevokedEvent(BaseModel):
    """Emitted when a certificate is revoked by an authorized user.

    Consumed by notification and audit systems that need to react
    to certificate revocations.

    Attributes:
        certificate_id: ID of the revoked certificate.
        revoked_by: User who performed the revocation.
        company_id: Tenant that owns the certificate.
        reason: Mandatory reason provided for the revocation.
    """

    pass
