"""Update course use case."""

from ...domain.entities import CourseEntity
from ...domain.exceptions import CourseNotFoundException
from ...domain.ports import CourseRepositoryPort


class UpdateCourseUseCase:
    """Apply changes to an existing course.

    Receives the full merged entity (Option B). Only the owning company
    can update a course.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseRepositoryPort) -> None:
        """Initialise with the course repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, entity: CourseEntity, updated_by: str) -> CourseEntity:
        """Persist the updated course entity.

        Args:
            entity: Merged course entity with new field values.
            updated_by: ULID of the user performing the update.

        Returns:
            CourseEntity: The updated entity after persistence.

        Raises:
            CourseNotFoundException: If the course does not exist.
        """
        existing = await self._repository.get_by_id_and_company(
            course_id=entity.id,
            company_id=entity.company_id,
        )
        if existing is None:
            raise CourseNotFoundException(course_id=entity.id)

        entity.updated_by = updated_by
        return await self._repository.update(entity)
