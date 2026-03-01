"""List certificates use case."""

from ...domain.entities import CertificateEntity
from ...domain.ports import CertificateRepositoryPort


class ListCertificatesUseCase:
    """Retrieves a paginated list of certificates for a given company.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CertificateRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self, company_id: str, page: int, page_size: int
    ) -> tuple[list[CertificateEntity], int]:
        """Execute the certificate list retrieval.

        Args:
            company_id: The ULID of the company whose certificates to list.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CertificateEntity, total count).
        """
        return await self._repository.list(
            company_id=company_id, page=page, page_size=page_size
        )
