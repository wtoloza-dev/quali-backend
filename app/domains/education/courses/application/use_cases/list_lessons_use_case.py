"""List lessons use case."""

from ...domain.entities import LessonEntity
from ...domain.ports import LessonRepositoryPort


class ListLessonsUseCase:
    """Return all lessons for a module, ordered by their order field.

    Public — no access check. Lesson titles and order are visible.
    Content is NOT included; use GetLessonUseCase for full content.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: LessonRepositoryPort) -> None:
        """Initialise with the lesson repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, module_id: str) -> list[LessonEntity]:
        """Return lessons for the given module sorted by order.

        Args:
            module_id: ULID of the parent module.

        Returns:
            List of LessonEntity sorted ascending by order.
        """
        return await self._repository.list_by_module(module_id=module_id)
