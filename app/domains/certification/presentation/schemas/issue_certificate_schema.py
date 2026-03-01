"""Issue certificate request schema."""

from datetime import datetime

from pydantic import BaseModel


class IssueCertificateRequestSchema(BaseModel):
    """Input schema for the issue certificate endpoint.

    Validates and deserializes the HTTP request body for certificate
    issuance. Only exposes fields that the API consumer is allowed to set.

    Attributes:
        recipient_id: ULID of the user receiving the certificate.
        title: Human-readable name of the certificate.
        description: Optional longer description of the certification.
        issued_at: Optional issuance timestamp — defaults to now if omitted.
        expires_at: Optional expiration timestamp.

    Note:
        The issuing company comes from the URL path, not the request body.
    """

    recipient_id: str
    title: str
    description: str | None = None
    issued_at: datetime | None = None
    expires_at: datetime | None = None
