"""Get company members use case."""

from ...domain.entities import CompanyMemberEntity
from ...domain.ports import CompanyMemberRepositoryPort


class GetCompanyMembersUseCase:
    """Retrieves all active members of a company.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyMemberRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, company_id: str) -> list[CompanyMemberEntity]:
        """Execute the get company members workflow.

        Args:
            company_id: ULID of the company whose members to retrieve.

        Returns:
            list[CompanyMemberEntity]: All active memberships for the company.
        """
        return await self._repository.get_by_company_id(company_id)
