"""Update lesson use case."""

from ...domain.entities import LessonEntity
from ...domain.exceptions import LessonNotFoundException
from ...domain.ports import LessonRepositoryPort


class UpdateLessonUseCase:
    """Apply changes to an existing lesson.

    Receives the full merged entity (Option B).

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: LessonRepositoryPort) -> None:
        """Initialise with the lesson repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, entity: LessonEntity, updated_by: str) -> LessonEntity:
        """Persist the updated lesson entity.

        Args:
            entity: Merged lesson entity with new field values.
            updated_by: ULID of the user performing the update.

        Returns:
            LessonEntity: The updated entity after persistence.

        Raises:
            LessonNotFoundException: If the lesson does not exist.
        """
        existing = await self._repository.get_by_id(entity.id)
        if existing is None:
            raise LessonNotFoundException(lesson_id=entity.id)

        entity.updated_by = updated_by
        return await self._repository.update(entity)
