"""Certificate response schemas."""

from datetime import datetime

from pydantic import BaseModel

from ...domain.enums import CertificateStatus


class CertificatePrivateResponseSchema(BaseModel):
    """Full certificate response for authenticated endpoints.

    Includes all fields including internal audit metadata and the
    verification token. Used for issue, get, revoke, and list endpoints.

    Attributes:
        id: ULID of the certificate.
        company_id: Tenant that issued the certificate.
        recipient_id: User who received the certificate.
        title: Human-readable name of the certificate.
        description: Optional longer description.
        token: Unique ULID token embedded in the QR code.
        status: Computed lifecycle status (active/expired/revoked).
        issued_at: When the certificate was officially issued.
        expires_at: Optional expiration timestamp.
        revoked_at: When the certificate was revoked, if applicable.
        revoked_by: ID of the revoking user, if applicable.
        revoked_reason: Reason for revocation, if applicable.
        created_at: DB-managed creation timestamp.
        created_by: ID of the user who created the record.
        updated_at: DB-managed last update timestamp.
        updated_by: ID of the user who last updated the record.
    """

    id: str
    company_id: str
    recipient_id: str
    title: str
    description: str | None
    token: str
    status: CertificateStatus
    issued_at: datetime
    expires_at: datetime | None
    revoked_at: datetime | None
    revoked_by: str | None
    revoked_reason: str | None
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None


class CertificateVerifyResponseSchema(BaseModel):
    """Public certificate response for the QR verification endpoint.

    Safe for unauthenticated access. Omits internal audit fields and
    exposes only the data needed to display the online certificate to
    anyone who scans the QR code.

    Attributes:
        id: ULID of the certificate.
        company_id: Tenant that issued the certificate.
        recipient_id: User who received the certificate.
        recipient_name: Full name of the recipient.
        recipient_document_type: Document type (CC, CE, etc.), if available.
        recipient_document_number: Document number, if available.
        title: Human-readable name of the certificate.
        description: Optional longer description.
        token: Unique ULID token for QR code display.
        status: Computed lifecycle status (active/expired/revoked).
        issued_at: When the certificate was officially issued.
        expires_at: Optional expiration timestamp.
        revoked_at: When the certificate was revoked, if applicable.
        revoked_reason: Public reason for revocation, if applicable.
    """

    id: str
    company_id: str
    recipient_id: str
    recipient_name: str
    recipient_document_type: str | None = None
    recipient_document_number: str | None = None
    title: str
    description: str | None
    token: str
    status: CertificateStatus
    issued_at: datetime
    expires_at: datetime | None
    revoked_at: datetime | None
    revoked_reason: str | None
