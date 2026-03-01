"""Delete course use case."""

from ...domain.exceptions import CourseNotFoundException
from ...domain.ports import CourseRepositoryPort


class DeleteCourseUseCase:
    """Hard-delete a course owned by the requesting company.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseRepositoryPort) -> None:
        """Initialise with the course repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, course_id: str, company_id: str, deleted_by: str) -> None:
        """Delete the course if it belongs to the given company.

        Args:
            course_id: ULID of the course to delete.
            company_id: Owning company — only the owner may delete.
            deleted_by: ULID of the user performing the deletion.

        Raises:
            CourseNotFoundException: If the course is not found or not owned by company.
        """
        course = await self._repository.get_by_id_and_company(
            course_id=course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=course_id)

        await self._repository.delete(course_id=course_id, deleted_by=deleted_by)
