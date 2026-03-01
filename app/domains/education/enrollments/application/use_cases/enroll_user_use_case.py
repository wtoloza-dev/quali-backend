"""Enroll user in a course use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import EnrollmentData, EnrollmentEntity
from ...domain.enums import EnrollmentStatus
from ...domain.ports import EnrollmentRepositoryPort


class EnrollUserUseCase:
    """Create a new course enrollment for a user.

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
        data: EnrollmentData,
        created_by: str,
    ) -> EnrollmentEntity:
        """Persist a new enrollment record.

        Args:
            data: Enrollment data specifying user, course, and company.
            created_by: ULID of the actor creating the enrollment.

        Returns:
            EnrollmentEntity: The persisted enrollment.
        """
        now = datetime.now(UTC)
        entity = EnrollmentEntity(
            id=str(ULID()),
            user_id=data.user_id,
            course_id=data.course_id,
            company_id=data.company_id,
            is_mandatory=data.is_mandatory,
            status=EnrollmentStatus.NOT_STARTED,
            enrolled_at=now,
            completed_at=None,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
