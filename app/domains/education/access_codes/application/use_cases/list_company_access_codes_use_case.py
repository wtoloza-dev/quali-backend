"""List company access codes use case."""

from app.shared.schemas.pagination_schema import PaginationParams

from ...domain.entities import AccessCodeEntity
from ...domain.ports import AccessCodeRepositoryPort


class ListCompanyAccessCodesUseCase:
    """Return a paginated list of all access codes for a company.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: AccessCodeRepositoryPort) -> None:
        """Initialise with the access code repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        company_id: str,
        params: PaginationParams,
    ) -> tuple[list[AccessCodeEntity], int]:
        """Return paginated access codes for all courses in a company.

        Args:
            company_id: ULID of the company.
            params: Pagination parameters.

        Returns:
            Tuple of (page of AccessCodeEntity, total count).
        """
        return await self._repository.list_by_company(
            company_id=company_id,
            page=params.page,
            page_size=params.page_size,
        )
