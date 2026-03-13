"""Enrollment repository port."""

from typing import Protocol

from ..entities import EnrollmentEntity


class EnrollmentRepositoryPort(Protocol):
    """Interface for the enrollment repository.

    Defined in the domain layer so use cases depend on this abstraction,
    not on the concrete SQLModel implementation.
    """

    async def save(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        """Persist a new enrollment and return the saved state.

        Args:
            entity: The enrollment entity to persist.

        Returns:
            EnrollmentEntity: The persisted entity with DB-generated fields.
        """
        ...

    async def get_by_id(self, enrollment_id: str) -> EnrollmentEntity | None:
        """Retrieve an enrollment by ULID.

        Args:
            enrollment_id: The ULID of the enrollment.

        Returns:
            EnrollmentEntity if found, None otherwise.
        """
        ...

    async def get_by_user_and_course(
        self, user_id: str, course_id: str
    ) -> EnrollmentEntity | None:
        """Return any enrollment for a user+course pair regardless of status.

        Args:
            user_id: The ULID of the user.
            course_id: The ULID of the course.

        Returns:
            EnrollmentEntity if found, None otherwise.
        """
        ...

    async def get_active_enrollment(
        self, user_id: str, course_id: str
    ) -> EnrollmentEntity | None:
        """Return the active (not_started or in_progress) enrollment for a user+course pair.

        Args:
            user_id: The ULID of the user.
            course_id: The ULID of the course.

        Returns:
            EnrollmentEntity if an active enrollment exists, None otherwise.
        """
        ...

    async def update(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        """Persist changes to an existing enrollment entity.

        Args:
            entity: The enrollment entity with updated fields.

        Returns:
            EnrollmentEntity: The updated entity after persistence.
        """
        ...

    async def delete(self, enrollment_id: str, deleted_by: str) -> None:
        """Hard-delete an enrollment and archive a tombstone snapshot.

        Args:
            enrollment_id: The ULID of the enrollment to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        ...

    async def list_by_user(
        self,
        user_id: str,
        page: int,
        page_size: int,
    ) -> tuple[list[EnrollmentEntity], int]:
        """Return paginated enrollments for a user.

        Args:
            user_id: The user whose enrollments to return.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of EnrollmentEntity, total count).
        """
        ...
