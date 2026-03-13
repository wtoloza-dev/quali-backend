"""Get company use case."""

from ...domain.entities import CompanyEntity
from ...domain.exceptions import CompanyNotFoundException
from ...domain.ports import CompanyRepositoryPort


class GetCompanyUseCase:
    """Retrieves a single company by its ULID identifier.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, company_id: str) -> CompanyEntity:
        """Execute the get company workflow.

        Accepts either a ULID or a slug. Tries by ID first, then falls
        back to slug lookup.

        Args:
            company_id: ULID or slug of the company to retrieve.

        Returns:
            CompanyEntity: The found company entity.

        Raises:
            CompanyNotFoundException: If no company exists with the given
                identifier.
        """
        entity = await self._repository.get_by_id(company_id)
        if entity is None:
            entity = await self._repository.get_by_slug(company_id)
        if entity is None:
            raise CompanyNotFoundException(company_id=company_id)
        return entity
