"""Get lesson use case."""

from ...domain.entities import LessonEntity
from ...domain.exceptions import LessonNotFoundException
from ...domain.ports import LessonRepositoryPort


class GetLessonUseCase:
    """Retrieve a single lesson by ID.

    Does not apply access control — the route layer resolves access
    and passes has_access to the mapper.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: LessonRepositoryPort) -> None:
        """Initialise with the lesson repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, lesson_id: str) -> LessonEntity:
        """Return the lesson entity.

        Args:
            lesson_id: ULID of the lesson to retrieve.

        Returns:
            LessonEntity: The found lesson.

        Raises:
            LessonNotFoundException: If the lesson does not exist.
        """
        lesson = await self._repository.get_by_id(lesson_id)
        if lesson is None:
            raise LessonNotFoundException(lesson_id=lesson_id)
        return lesson
