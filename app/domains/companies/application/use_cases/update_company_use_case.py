"""Update company use case."""

from ...domain.entities import CompanyEntity
from ...domain.ports import CompanyRepositoryPort


class UpdateCompanyUseCase:
    """Persists a fully merged company entity.

    The caller (presentation layer) is responsible for fetching the existing
    entity, applying the patch, and passing the result here. Slug is immutable
    and is never included in updates, so no conflict check is needed.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, entity: CompanyEntity) -> CompanyEntity:
        """Persist the updated entity.

        Args:
            entity: Fully merged company entity ready to be persisted.

        Returns:
            CompanyEntity: The updated entity after persistence.
        """
        return await self._repository.update(entity)
