"""Update enrollment status use case."""

from datetime import UTC, datetime

from ...domain.entities import EnrollmentEntity
from ...domain.enums import EnrollmentStatus
from ...domain.exceptions import EnrollmentNotFoundException
from ...domain.ports import EnrollmentRepositoryPort


class UpdateEnrollmentStatusUseCase:
    """Advance the status of an enrollment.

    Sets completed_at automatically when the enrollment is marked
    as completed or failed.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: EnrollmentRepositoryPort) -> None:
        """Initialise with the enrollment repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        enrollment_id: str,
        status: EnrollmentStatus,
        updated_by: str,
    ) -> EnrollmentEntity:
        """Update the status of an enrollment.

        Args:
            enrollment_id: ULID of the enrollment to update.
            status: The new enrollment status.
            updated_by: ULID of the actor performing the update.

        Returns:
            EnrollmentEntity: The updated enrollment.

        Raises:
            EnrollmentNotFoundException: If no enrollment with that ID exists.
        """
        entity = await self._repository.get_by_id(enrollment_id)
        if entity is None:
            raise EnrollmentNotFoundException(enrollment_id)

        new_status = entity.status.transition_to(status)

        completed_at = entity.completed_at
        if new_status in (EnrollmentStatus.COMPLETED, EnrollmentStatus.FAILED):
            if completed_at is None:
                completed_at = datetime.now(UTC)

        updated = entity.model_copy(
            update={
                "status": new_status,
                "completed_at": completed_at,
                "updated_by": updated_by,
            }
        )
        return await self._repository.update(updated)
