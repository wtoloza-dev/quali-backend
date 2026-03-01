"""List modules use case."""

from ...domain.entities import ModuleEntity
from ...domain.ports import ModuleRepositoryPort


class ListModulesUseCase:
    """Return all modules for a course, ordered by their order field.

    Public — no access check. Any user (including unauthenticated) can
    see module titles and order. Lesson content is gated separately.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: ModuleRepositoryPort) -> None:
        """Initialise with the module repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, course_id: str) -> list[ModuleEntity]:
        """Return modules for the given course sorted by order.

        Args:
            course_id: ULID of the parent course.

        Returns:
            List of ModuleEntity sorted ascending by order.
        """
        return await self._repository.list_by_course(course_id=course_id)
