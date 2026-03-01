"""Unenroll (delete enrollment) use case."""

from ...domain.exceptions import EnrollmentNotFoundException
from ...domain.ports import EnrollmentRepositoryPort


class UnenrollUseCase:
    """Remove an enrollment record.

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
        self, enrollment_id: str, company_id: str, deleted_by: str
    ) -> None:
        """Hard-delete an enrollment, writing a tombstone for audit.

        Args:
            enrollment_id: ULID of the enrollment to remove.
            company_id: ULID of the owning company for tenant scoping.
            deleted_by: ULID of the actor performing the deletion.

        Raises:
            EnrollmentNotFoundException: If no enrollment with that ID
                exists within the given company.
        """
        entity = await self._repository.get_by_id_and_company(enrollment_id, company_id)
        if entity is None:
            raise EnrollmentNotFoundException(enrollment_id)
        await self._repository.delete(enrollment_id, deleted_by)
