"""List assessment attempts use case."""

from app.domains.education.enrollments.domain.ports import EnrollmentRepositoryPort
from app.shared.exceptions import ForbiddenException, NotFoundException

from ...domain.entities import AttemptEntity
from ...domain.ports import AttemptRepositoryPort


class ListAttemptsUseCase:
    """Return all attempts for an enrollment owned by the authenticated user.

    Args:
        repository: Port implementation provided by the infrastructure layer.
        enrollment_repository: Enrollment port to verify ownership.
    """

    def __init__(
        self,
        repository: AttemptRepositoryPort,
        enrollment_repository: EnrollmentRepositoryPort,
    ) -> None:
        """Initialise with the attempt and enrollment repositories.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
            enrollment_repository: Enrollment repository for ownership checks.
        """
        self._repository = repository
        self._enrollment_repository = enrollment_repository

    async def execute(
        self,
        enrollment_id: str,
        user_id: str,
    ) -> list[AttemptEntity]:
        """Return all attempts for an enrollment after verifying ownership.

        Args:
            enrollment_id: ULID of the enrollment whose attempts to list.
            user_id: ULID of the authenticated user.

        Returns:
            List of AttemptEntity sorted by attempt_number ascending.

        Raises:
            NotFoundException: If the enrollment does not exist.
            ForbiddenException: If the enrollment does not belong to the user.
        """
        enrollment = await self._enrollment_repository.get_by_id(enrollment_id)
        if enrollment is None:
            raise NotFoundException(
                message="Enrollment not found.",
                context={"enrollment_id": enrollment_id},
                error_code="ENROLLMENT_NOT_FOUND",
            )
        if enrollment.user_id != user_id:
            raise ForbiddenException(
                message="You do not have access to this enrollment.",
                context={"enrollment_id": enrollment_id},
                error_code="ENROLLMENT_ACCESS_DENIED",
            )
        return await self._repository.list_by_enrollment(
            enrollment_id=enrollment_id,
        )
