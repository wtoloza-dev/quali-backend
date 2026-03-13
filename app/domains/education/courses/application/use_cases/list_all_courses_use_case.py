"""List all courses use case."""

from ...domain.entities import CourseEntity
from ...domain.ports import CourseRepositoryPort


class ListAllCoursesUseCase:
    """Return a paginated list of all courses across all companies.

    Intended for superadmin use only — authorisation is enforced at the
    route layer.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseRepositoryPort) -> None:
        """Initialise with the course repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        page: int,
        page_size: int,
    ) -> tuple[list[CourseEntity], int]:
        """Return a page of all courses.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CourseEntity, total count).
        """
        return await self._repository.list_all(
            page=page,
            page_size=page_size,
        )
