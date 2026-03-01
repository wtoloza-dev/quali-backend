"""List courses use case."""

from ...domain.entities import CourseEntity
from ...domain.ports import CourseRepositoryPort


class ListCoursesUseCase:
    """Return a paginated list of courses visible to a company.

    Includes the company's own courses and all public courses.

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
        company_id: str,
    ) -> tuple[list[CourseEntity], int]:
        """Return a page of courses visible to the requesting company.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.
            company_id: ID of the requesting company.

        Returns:
            Tuple of (list of CourseEntity, total count).
        """
        return await self._repository.list(
            page=page,
            page_size=page_size,
            company_id=company_id,
        )
