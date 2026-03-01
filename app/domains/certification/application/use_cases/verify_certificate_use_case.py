"""Verify certificate use case."""

from ...domain.entities import CertificateEntity
from ...domain.exceptions import CertificateNotFoundException
from ...domain.ports import CertificateRepositoryPort


class VerifyCertificateUseCase:
    """Retrieves and validates a certificate by its QR verification token.

    Public use case — no authentication required. Used when a physical
    certificate QR code is scanned and the holder navigates to the
    verification page.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CertificateRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, token: str) -> CertificateEntity:
        """Execute the certificate verification workflow.

        Args:
            token: The unique ULID token embedded in the QR code.

        Returns:
            CertificateEntity: The found certificate entity with computed status.

        Raises:
            CertificateNotFoundException: If no certificate matches the given token.
        """
        certificate = await self._repository.get_by_token(token)
        if certificate is None:
            raise CertificateNotFoundException(certificate_id=token)
        return certificate
