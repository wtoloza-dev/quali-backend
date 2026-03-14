"""Admin list assessment attempts use case."""

from ...domain.entities import AttemptEntity
from ...domain.ports import AttemptRepositoryPort


class AdminListAttemptsUseCase:
    """Return all attempts for an enrollment without ownership checks.

    Intended for admin-level access where the caller has already been
    authorised via ``require_role(Role.ADMIN)``.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: AttemptRepositoryPort) -> None:
        """Initialise with the attempt repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, enrollment_id: str) -> list[AttemptEntity]:
        """Return all attempts for an enrollment.

        Args:
            enrollment_id: ULID of the enrollment whose attempts to list.

        Returns:
            List of AttemptEntity sorted by attempt_number ascending.
        """
        return await self._repository.list_by_enrollment(
            enrollment_id=enrollment_id,
        )
