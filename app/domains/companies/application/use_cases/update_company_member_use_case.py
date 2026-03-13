"""Update company member use case."""

from ...domain.entities import CompanyMemberEntity
from ...domain.ports import CompanyMemberRepositoryPort


class UpdateCompanyMemberUseCase:
    """Handles updating a company member's role.

    Fetches the existing membership by company and user IDs, updates the
    role field, and persists the change via the repository.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyMemberRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, entity: CompanyMemberEntity) -> CompanyMemberEntity:
        """Persist the updated company member entity.

        Args:
            entity: Fully merged company member entity ready to be persisted.

        Returns:
            CompanyMemberEntity: The updated entity after persistence.
        """
        return await self._repository.update(entity)
