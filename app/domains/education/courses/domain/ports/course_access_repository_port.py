"""Course access repository port."""

from typing import Protocol

from ..entities import CourseAccessEntity


class CourseAccessRepositoryPort(Protocol):
    """Interface for the course access repository."""

    async def save(self, entity: CourseAccessEntity) -> CourseAccessEntity:
        """Persist a new course access record.

        Args:
            entity: The course access entity to persist.

        Returns:
            CourseAccessEntity: The persisted entity.
        """
        ...

    async def get_active_access(
        self, user_id: str, course_id: str
    ) -> CourseAccessEntity | None:
        """Return the active (non-expired) access record for a user+course pair.

        Args:
            user_id: The user's ULID.
            course_id: The course's ULID.

        Returns:
            CourseAccessEntity if active access exists, None otherwise.
        """
        ...
