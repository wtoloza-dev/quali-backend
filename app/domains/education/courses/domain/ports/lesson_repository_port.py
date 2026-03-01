"""Lesson repository port."""

from typing import Protocol

from ..entities import LessonEntity


class LessonRepositoryPort(Protocol):
    """Interface for the lesson repository."""

    async def save(self, entity: LessonEntity) -> LessonEntity:
        """Persist a new lesson and return the saved state.

        Args:
            entity: The lesson entity to persist.

        Returns:
            LessonEntity: The persisted entity.
        """
        ...

    async def get_by_id(self, lesson_id: str) -> LessonEntity | None:
        """Retrieve a lesson by ULID.

        Args:
            lesson_id: The ULID of the lesson.

        Returns:
            LessonEntity if found, None otherwise.
        """
        ...

    async def list_by_module(self, module_id: str) -> list[LessonEntity]:
        """Return all lessons for a module ordered by their order field.

        Args:
            module_id: The ULID of the parent module.

        Returns:
            List of LessonEntity sorted by order ascending.
        """
        ...

    async def update(self, entity: LessonEntity) -> LessonEntity:
        """Persist changes to an existing lesson entity.

        Args:
            entity: The lesson entity with updated fields.

        Returns:
            LessonEntity: The updated entity after persistence.
        """
        ...

    async def delete(self, lesson_id: str, deleted_by: str) -> None:
        """Hard-delete a lesson and archive a tombstone snapshot.

        Args:
            lesson_id: The ULID of the lesson to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        ...

    async def update_order(self, lesson_id: str, order: int) -> None:
        """Update only the order field of a lesson.

        Args:
            lesson_id: The ULID of the lesson.
            order: The new order value.
        """
        ...
