"""Enroll user in a course use case."""

from datetime import UTC, datetime, timedelta

from ulid import ULID

from app.domains.education.courses.domain.ports import CourseRepositoryPort

from ...domain.entities import EnrollmentData, EnrollmentEntity
from ...domain.enums import EnrollmentStatus
from ...domain.ports import EnrollmentRepositoryPort


class EnrollUserUseCase:
    """Create a new course enrollment for a user.

    If the user already has an enrollment for the course, returns the
    existing one. If the enrollment is completed and the course validity
    period has expired, resets the enrollment for a fresh attempt.

    Args:
        repository: Port implementation provided by the infrastructure layer.
        course_repository: Course port to check validity_days.
    """

    def __init__(
        self,
        repository: EnrollmentRepositoryPort,
        course_repository: CourseRepositoryPort,
    ) -> None:
        """Initialise with the enrollment and course repositories.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
            course_repository: Course repository to look up validity_days.
        """
        self._repository = repository
        self._course_repository = course_repository

    async def execute(
        self,
        data: EnrollmentData,
        created_by: str,
    ) -> EnrollmentEntity:
        """Persist a new enrollment or return/reset an existing one.

        Args:
            data: Enrollment data specifying user, course, and company.
            created_by: ULID of the actor creating the enrollment.

        Returns:
            EnrollmentEntity: The persisted, existing, or reset enrollment.
        """
        existing = await self._repository.get_by_user_and_course(
            user_id=data.user_id,
            course_id=data.course_id,
        )

        if existing is not None:
            # If completed and expired, reset for re-enrollment
            if existing.status == EnrollmentStatus.COMPLETED and existing.completed_at:
                course = await self._course_repository.get_by_id(data.course_id)
                validity_days = course.validity_days if course else 365
                expiry = existing.completed_at + timedelta(days=validity_days)
                if datetime.now(UTC) >= expiry:
                    now = datetime.now(UTC)
                    reset = existing.model_copy(
                        update={
                            "status": EnrollmentStatus.NOT_STARTED,
                            "enrolled_at": now,
                            "completed_at": None,
                            "updated_by": created_by,
                        }
                    )
                    return await self._repository.update(reset)

            return existing

        now = datetime.now(UTC)
        entity = EnrollmentEntity(
            id=str(ULID()),
            user_id=data.user_id,
            course_id=data.course_id,
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
