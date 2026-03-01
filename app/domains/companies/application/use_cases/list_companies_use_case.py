"""List companies use case."""

from ...domain.entities import CompanyEntity
from ...domain.ports import CompanyRepositoryPort


class ListCompaniesUseCase:
    """Retrieve a paginated list of companies.

    Delegates pagination entirely to the repository and returns
    the result tuple to the presentation layer unchanged.

    Attributes:
        _repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self, page: int, page_size: int
    ) -> tuple[list[CompanyEntity], int]:
        """Return a page of companies and the total record count.

        Args:
            page: 1-based page number to retrieve.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CompanyEntity for the requested page, total count).
        """
        return await self._repository.list(page=page, page_size=page_size)
