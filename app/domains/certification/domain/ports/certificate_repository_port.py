"""Certificate repository port."""

from typing import Protocol

from ..entities import CertificateEntity


class CertificateRepositoryPort(Protocol):
    """Interface for the certificate repository.

    Defined in the domain layer so the application layer depends on this
    abstraction, not on the concrete SQLModel implementation. The
    infrastructure layer provides the real implementation.
    """

    async def save(self, entity: CertificateEntity) -> CertificateEntity:
        """Persist a certificate entity and return the saved state.

        Args:
            entity: The certificate entity to persist.

        Returns:
            CertificateEntity: The persisted entity with any DB-generated fields.
        """
        ...

    async def get_by_id(self, certificate_id: str) -> CertificateEntity | None:
        """Retrieve a certificate by its ULID identifier.

        Args:
            certificate_id: The ULID of the certificate.

        Returns:
            CertificateEntity if found, None otherwise.
        """
        ...

    async def get_by_id_and_company(
        self, certificate_id: str, company_id: str
    ) -> CertificateEntity | None:
        """Retrieve a certificate scoped to a specific company.

        Returns None if the certificate does not exist or belongs to a
        different company, preventing cross-tenant data access.

        Args:
            certificate_id: The ULID of the certificate.
            company_id: The ULID of the owning company.

        Returns:
            CertificateEntity if found within the company, None otherwise.
        """
        ...

    async def get_by_token(self, token: str) -> CertificateEntity | None:
        """Retrieve a certificate by its unique verification token.

        Args:
            token: The ULID token embedded in the QR code.

        Returns:
            CertificateEntity if found, None otherwise.
        """
        ...

    async def update(self, entity: CertificateEntity) -> CertificateEntity:
        """Persist changes to an existing certificate entity.

        Args:
            entity: The certificate entity with updated fields.

        Returns:
            CertificateEntity: The updated entity reflecting the persisted state.
        """
        ...

    async def list(
        self, company_id: str, page: int, page_size: int
    ) -> tuple[list[CertificateEntity], int]:
        """Retrieve a paginated slice of certificates for a company.

        Args:
            company_id: The ULID of the company whose certificates to list.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CertificateEntity, total count).
        """
        ...

    async def list_by_recipient(
        self, recipient_id: str, page: int, page_size: int
    ) -> tuple[list[CertificateEntity], int]:
        """Retrieve a paginated slice of certificates for a recipient.

        Args:
            recipient_id: The Firebase UID of the certificate recipient.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CertificateEntity, total count).
        """
        ...
