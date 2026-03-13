"""Check course access use case."""

from datetime import UTC, datetime

from app.domains.education.enrollments.domain.enums import AccessType
from app.domains.education.enrollments.domain.ports import EnrollmentRepositoryPort


class CheckCourseAccessUseCase:
    """Determine whether a user has active full access to a course.

    Checks the enrollment table for FULL access_type with a valid
    (non-expired) date range.

    Args:
        enrollment_repository: Enrollment port to look up access.
    """

    def __init__(self, enrollment_repository: EnrollmentRepositoryPort) -> None:
        """Initialise with the enrollment repository.

        Args:
            enrollment_repository: Concrete repository injected by the infrastructure layer.
        """
        self._enrollment_repository = enrollment_repository

    async def execute(self, user_id: str, course_id: str) -> bool:
        """Return True if the user has active full access to the course.

        Args:
            user_id: ULID of the user.
            course_id: ULID of the course.

        Returns:
            bool: True if the user has non-expired FULL access.
        """
        enrollment = await self._enrollment_repository.get_by_user_and_course(
            user_id=user_id,
            course_id=course_id,
        )
        if enrollment is None:
            return False

        if enrollment.access_type != AccessType.FULL:
            return False

        # Check expiration if end_date is set.
        if enrollment.end_date is not None:
            return datetime.now(UTC) < enrollment.end_date

        return True
