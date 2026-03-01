"""List enrollments use case."""

from app.shared.schemas.pagination_schema import PaginationParams

from ...domain.entities import EnrollmentEntity
from ...domain.ports import EnrollmentRepositoryPort


class ListEnrollmentsUseCase:
    """Return a paginated list of enrollments for a company.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: EnrollmentRepositoryPort) -> None:
        """Initialise with the enrollment repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        company_id: str,
        params: PaginationParams,
    ) -> tuple[list[EnrollmentEntity], int]:
        """Return paginated enrollments for the given company.

        Args:
            company_id: ULID of the company to scope the listing.
            params: Pagination parameters.

        Returns:
            Tuple of (page of EnrollmentEntity, total count).
        """
        return await self._repository.list_by_company(
            company_id=company_id,
            page=params.page,
            page_size=params.page_size,
        )
