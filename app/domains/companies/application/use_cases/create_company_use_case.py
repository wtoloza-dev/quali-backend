"""Create company use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import CompanyData, CompanyEntity
from ...domain.exceptions import CompanySlugTakenException
from ...domain.ports import CompanyRepositoryPort


class CreateCompanyUseCase:
    """Handles the registration of a new company.

    Validates that the slug is not already taken, constructs the company
    entity, persists it via the repository, and emits a CompanyCreatedEvent.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, data: CompanyData, created_by: str) -> CompanyEntity:
        """Execute the company creation workflow.

        Args:
            data: Validated company data from the presentation layer.
            created_by: ULID of the authenticated user creating the company.

        Returns:
            CompanyEntity: The persisted company entity.

        Raises:
            CompanySlugTakenException: If a company with the same slug already exists.
        """
        existing = await self._repository.get_by_slug(data.slug)
        if existing:
            raise CompanySlugTakenException(slug=data.slug)

        now = datetime.now(UTC)
        entity = CompanyEntity(
            id=str(ULID()),
            name=data.name,
            slug=data.slug,
            company_type=data.company_type,
            email=data.email,
            country=data.country,
            tax=data.tax,
            legal_name=data.legal_name,
            logo_url=data.logo_url,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
