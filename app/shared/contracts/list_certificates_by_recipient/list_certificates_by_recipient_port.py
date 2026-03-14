"""list_certificates_by_recipient contract port.

Defines the minimal interface and return type for listing certificates
by recipient across domain boundaries. Any domain that needs to look up
certificates depends only on this module — never on the certification
domain directly.
"""

from datetime import datetime
from typing import Protocol

from pydantic import BaseModel


class CertificateContractResult(BaseModel):
    """Minimal certificate projection for cross-domain consumers."""

    id: str
    company_id: str
    recipient_id: str
    title: str
    description: str | None
    token: str
    status: str
    issued_at: datetime
    expires_at: datetime | None
    revoked_at: datetime | None


class CertificateListContractResult(BaseModel):
    """Paginated certificate list for cross-domain consumers."""

    items: list[CertificateContractResult]
    total: int
    page: int
    page_size: int
    pages: int


class ListCertificatesByRecipientPort(Protocol):
    """Contract interface for listing certificates by recipient ID."""

    async def __call__(
        self, recipient_id: str, page: int, page_size: int
    ) -> CertificateListContractResult:
        """Retrieve a paginated list of certificates for a recipient.

        Args:
            recipient_id: The Firebase UID of the certificate recipient.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            CertificateListContractResult with items and pagination metadata.
        """
        ...
