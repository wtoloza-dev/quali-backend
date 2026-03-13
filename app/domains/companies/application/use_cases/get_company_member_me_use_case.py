"""Get current user's company membership use case."""

from ...domain.entities import CompanyMemberEntity
from ...domain.ports import CompanyMemberRepositoryPort


class GetCompanyMemberMeUseCase:
    """Retrieves the current user's membership in a specific company.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyMemberRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self, company_id: str, user_id: str
    ) -> CompanyMemberEntity | None:
        """Execute the get company member me workflow.

        Args:
            company_id: ULID of the company.
            user_id: ULID of the authenticated user.

        Returns:
            CompanyMemberEntity if the user is a member, None otherwise.
        """
        return await self._repository.get_by_company_and_user(company_id, user_id)
