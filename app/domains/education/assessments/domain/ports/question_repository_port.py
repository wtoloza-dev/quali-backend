"""Question repository port."""

from typing import Protocol

from ..entities import QuestionEntity


class QuestionRepositoryPort(Protocol):
    """Interface for the question repository."""

    async def save(self, entity: QuestionEntity) -> QuestionEntity:
        """Persist a new question and return the saved state.

        Args:
            entity: The question entity to persist.

        Returns:
            QuestionEntity: The persisted entity.
        """
        ...

    async def get_by_id(self, question_id: str) -> QuestionEntity | None:
        """Retrieve a question by ULID.

        Args:
            question_id: The ULID of the question.

        Returns:
            QuestionEntity if found, None otherwise.
        """
        ...

    async def list_by_course(self, course_id: str) -> list[QuestionEntity]:
        """Return all questions for a course ordered by their display order.

        Args:
            course_id: The ULID of the course.

        Returns:
            List of QuestionEntity sorted by order ascending.
        """
        ...

    async def list_by_module(self, module_id: str) -> list[QuestionEntity]:
        """Return all questions for a module ordered by their display order.

        Args:
            module_id: The ULID of the module.

        Returns:
            List of QuestionEntity sorted by order ascending.
        """
        ...

    async def delete(self, question_id: str, deleted_by: str) -> None:
        """Hard-delete a question after saving a tombstone snapshot.

        Args:
            question_id: The ULID of the question to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        ...
