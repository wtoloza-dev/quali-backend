"""Reset attempts use case."""

from app.domains.education.enrollments.domain.enums import EnrollmentStatus
from app.domains.education.enrollments.domain.ports import EnrollmentRepositoryPort
from app.shared.exceptions import NotFoundException

from ...domain.ports import AttemptRepositoryPort


class ResetAttemptsUseCase:
    """Delete attempts for an enrollment, optionally scoped to a module.

    When module_id is provided, only that module's attempts are deleted
    and the enrollment status is not changed. When module_id is omitted,
    all attempts are deleted and the enrollment resets to not_started.

    Attributes:
        _attempt_repository: Port for attempt persistence.
        _enrollment_repository: Port for enrollment persistence.
    """

    def __init__(
        self,
        attempt_repository: AttemptRepositoryPort,
        enrollment_repository: EnrollmentRepositoryPort,
    ) -> None:
        """Initialise with repository ports.

        Args:
            attempt_repository: Attempt repository port.
            enrollment_repository: Enrollment repository port.
        """
        self._attempt_repository = attempt_repository
        self._enrollment_repository = enrollment_repository

    async def execute(
        self,
        enrollment_id: str,
        reset_by: str,
        module_id: str | None = None,
    ) -> int:
        """Delete attempts and optionally reset the enrollment status.

        Args:
            enrollment_id: ULID of the enrollment to reset.
            reset_by: ULID of the admin performing the reset.
            module_id: If provided, only reset attempts for this module.

        Returns:
            Number of deleted attempts.

        Raises:
            NotFoundException: If the enrollment does not exist.
        """
        enrollment = await self._enrollment_repository.get_by_id(enrollment_id)
        if enrollment is None:
            raise NotFoundException(
                message="Enrollment not found.",
                context={"enrollment_id": enrollment_id},
                error_code="ENROLLMENT_NOT_FOUND",
            )

        if module_id:
            deleted_count = (
                await self._attempt_repository.delete_by_enrollment_and_module(
                    enrollment_id=enrollment_id,
                    module_id=module_id,
                    deleted_by=reset_by,
                )
            )
        else:
            deleted_count = await self._attempt_repository.delete_by_enrollment(
                enrollment_id=enrollment_id,
                deleted_by=reset_by,
            )
            if enrollment.status != EnrollmentStatus.NOT_STARTED:
                enrollment.status = EnrollmentStatus.NOT_STARTED
                enrollment.completed_at = None
                enrollment.updated_by = reset_by
                await self._enrollment_repository.update(enrollment)

        return deleted_count
