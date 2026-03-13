"""Get enrollment use case."""

from ...domain.entities import EnrollmentEntity
from ...domain.exceptions import EnrollmentNotFoundException
from ...domain.ports import EnrollmentRepositoryPort


class GetEnrollmentUseCase:
    """Retrieve a single enrollment by its ULID.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: EnrollmentRepositoryPort) -> None:
        """Initialise with the enrollment repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, enrollment_id: str) -> EnrollmentEntity:
        """Retrieve an enrollment by ID.

        Args:
            enrollment_id: ULID of the enrollment to retrieve.

        Returns:
            EnrollmentEntity: The matching enrollment.

        Raises:
            EnrollmentNotFoundException: If no enrollment with that ID exists.
        """
        entity = await self._repository.get_by_id(enrollment_id)
        if entity is None:
            raise EnrollmentNotFoundException(enrollment_id)
        return entity
