"""List enrollments use case."""

from app.shared.schemas.pagination_schema import PaginationParams

from ...domain.entities import EnrollmentEntity
from ...domain.ports import EnrollmentRepositoryPort


class ListEnrollmentsUseCase:
    """Return a paginated list of enrollments for a user.

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
        user_id: str,
        params: PaginationParams,
    ) -> tuple[list[EnrollmentEntity], int]:
        """Return paginated enrollments for a user.

        Args:
            user_id: ULID of the authenticated user.
            params: Pagination parameters.

        Returns:
            Tuple of (page of EnrollmentEntity, total count).
        """
        return await self._repository.list_by_user(
            user_id=user_id,
            page=params.page,
            page_size=params.page_size,
        )
