"""Remove company member use case."""

from ...domain.exceptions import CompanyMemberNotFoundException
from ...domain.ports import CompanyMemberRepositoryPort


class RemoveCompanyMemberUseCase:
    """Hard-deletes a company membership and archives a tombstone snapshot for audit purposes.

    Validates that the membership exists before performing the deletion.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyMemberRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, company_id: str, user_id: str, deleted_by: str) -> None:
        """Execute the remove company member workflow.

        Args:
            company_id: ULID of the company.
            user_id: ULID of the user to remove.
            deleted_by: ID of the actor performing the removal.

        Raises:
            CompanyMemberNotFoundException: If no active membership exists for the pair.
        """
        entity = await self._repository.get_by_company_and_user(
            company_id=company_id,
            user_id=user_id,
        )
        if entity is None:
            raise CompanyMemberNotFoundException(
                user_id=user_id,
                company_id=company_id,
            )

        await self._repository.delete(
            company_member_id=entity.id,
            deleted_by=deleted_by,
        )
