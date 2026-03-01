"""Revoke certificate use case."""

from datetime import UTC, datetime

from ...domain.entities import CertificateEntity
from ...domain.exceptions import (
    CertificateAlreadyRevokedException,
    CertificateNotFoundException,
)
from ...domain.ports import CertificateRepositoryPort


class RevokeCertificateUseCase:
    """Handles the revocation of an active digital certificate.

    Validates that the certificate exists and is not already revoked,
    then persists the revocation state via the repository.

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
        self, certificate_id: str, company_id: str, revoked_by: str, reason: str
    ) -> CertificateEntity:
        """Execute the certificate revocation workflow.

        Args:
            certificate_id: The ULID of the certificate to revoke.
            company_id: The ULID of the company that must own the certificate.
            revoked_by: The ULID of the user performing the revocation.
            reason: Mandatory reason for the revocation.

        Returns:
            CertificateEntity: The updated certificate entity after revocation.

        Raises:
            CertificateNotFoundException: If no certificate matches the ID and company.
            CertificateAlreadyRevokedException: If the certificate is already revoked.
        """
        certificate = await self._repository.get_by_id_and_company(
            certificate_id=certificate_id, company_id=company_id
        )
        if certificate is None:
            raise CertificateNotFoundException(certificate_id=certificate_id)
        if not certificate.is_revokable:
            raise CertificateAlreadyRevokedException(certificate_id=certificate_id)

        revoked = certificate.model_copy(
            update={
                "revoked_at": datetime.now(UTC),
                "revoked_by": revoked_by,
                "revoked_reason": reason,
                "updated_by": revoked_by,
            }
        )
        return await self._repository.update(revoked)
