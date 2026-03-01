"""Get certificate use case."""

from ...domain.entities import CertificateEntity
from ...domain.exceptions import CertificateNotFoundException
from ...domain.ports import CertificateRepositoryPort


class GetCertificateUseCase:
    """Retrieves a single certificate by its ULID identifier.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CertificateRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, certificate_id: str, company_id: str) -> CertificateEntity:
        """Execute the certificate retrieval workflow.

        Args:
            certificate_id: The ULID of the certificate to retrieve.
            company_id: The ULID of the company that must own the certificate.

        Returns:
            CertificateEntity: The found certificate entity.

        Raises:
            CertificateNotFoundException: If no certificate matches the ID and company.
        """
        certificate = await self._repository.get_by_id_and_company(
            certificate_id=certificate_id, company_id=company_id
        )
        if certificate is None:
            raise CertificateNotFoundException(certificate_id=certificate_id)
        return certificate
