"""Attempt repository port."""

from typing import Protocol

from ..entities import AttemptEntity


class AttemptRepositoryPort(Protocol):
    """Interface for the assessment attempt repository."""

    async def save(self, entity: AttemptEntity) -> AttemptEntity:
        """Persist a new attempt and return the saved state.

        Args:
            entity: The attempt entity to persist.

        Returns:
            AttemptEntity: The persisted entity.
        """
        ...

    async def count_by_enrollment(self, enrollment_id: str) -> int:
        """Count the number of attempts for a given enrollment.

        Args:
            enrollment_id: The ULID of the enrollment.

        Returns:
            Number of existing attempts.
        """
        ...

    async def count_by_enrollment_and_module(
        self, enrollment_id: str, module_id: str
    ) -> int:
        """Count attempts for a given enrollment and module.

        Args:
            enrollment_id: The ULID of the enrollment.
            module_id: The ULID of the module.

        Returns:
            Number of existing attempts for that module.
        """
        ...

    async def list_by_enrollment(self, enrollment_id: str) -> list[AttemptEntity]:
        """Return all attempts for an enrollment ordered by attempt_number.

        Args:
            enrollment_id: The ULID of the enrollment.

        Returns:
            List of AttemptEntity sorted by attempt_number ascending.
        """
        ...

    async def delete_by_enrollment(self, enrollment_id: str, deleted_by: str) -> int:
        """Delete all attempts for an enrollment and archive tombstones.

        Args:
            enrollment_id: The ULID of the enrollment.
            deleted_by: ULID of the user performing the deletion.

        Returns:
            Number of deleted attempts.
        """
        ...

    async def delete_by_enrollment_and_module(
        self, enrollment_id: str, module_id: str, deleted_by: str
    ) -> int:
        """Delete attempts for a specific module within an enrollment.

        Args:
            enrollment_id: The ULID of the enrollment.
            module_id: The ULID of the module.
            deleted_by: ULID of the user performing the deletion.

        Returns:
            Number of deleted attempts.
        """
        ...
