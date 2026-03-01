"""Delete company use case."""

from ...domain.exceptions import CompanyNotFoundException
from ...domain.ports import CompanyRepositoryPort


class DeleteCompanyUseCase:
    """Hard-deletes a company and archives a tombstone snapshot for audit purposes.

    Validates that the company exists before performing the deletion.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, company_id: str, deleted_by: str) -> None:
        """Execute the delete company workflow.

        Args:
            company_id: ULID of the company to delete.
            deleted_by: ULID of the authenticated user performing the deletion.

        Raises:
            CompanyNotFoundException: If no company exists with the given ID.
        """
        entity = await self._repository.get_by_id(company_id)
        if entity is None:
            raise CompanyNotFoundException(company_id=company_id)

        await self._repository.delete(
            company_id=company_id,
            deleted_by=deleted_by,
        )
