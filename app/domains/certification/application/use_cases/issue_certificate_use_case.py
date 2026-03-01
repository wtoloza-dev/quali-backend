"""Issue certificate use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import CertificateData, CertificateEntity
from ...domain.ports import CertificateRepositoryPort


class IssueCertificateUseCase:
    """Handles the creation and issuance of a new digital certificate.

    Constructs the certificate entity with a unique verification token,
    persists it via the repository, and returns the saved entity.

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
        self, data: CertificateData, created_by: str
    ) -> CertificateEntity:
        """Execute the certificate issuance workflow.

        Args:
            data: Validated certificate data from the presentation layer.
            created_by: ULID of the authenticated user issuing the certificate.

        Returns:
            CertificateEntity: The persisted certificate entity.
        """
        now = datetime.now(UTC)
        entity = CertificateEntity(
            id=str(ULID()),
            token=str(ULID()),
            company_id=data.company_id,
            recipient_id=data.recipient_id,
            title=data.title,
            description=data.description,
            issued_at=data.issued_at if data.issued_at is not None else now,
            expires_at=data.expires_at,
            revoked_at=None,
            revoked_by=None,
            revoked_reason=None,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
