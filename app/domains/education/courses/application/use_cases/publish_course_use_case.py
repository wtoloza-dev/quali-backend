"""Publish course use case."""

from ...domain.entities import CourseEntity
from ...domain.enums import CourseStatus
from ...domain.exceptions import CourseNotFoundException
from ...domain.ports import CourseRepositoryPort


class PublishCourseUseCase:
    """Transition a course from DRAFT to PUBLISHED status.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseRepositoryPort) -> None:
        """Initialise with the course repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self, course_id: str, company_id: str, updated_by: str
    ) -> CourseEntity:
        """Set the course status to PUBLISHED.

        Args:
            course_id: ULID of the course to publish.
            company_id: Owning company — only the owner may publish.
            updated_by: ULID of the user performing the action.

        Returns:
            CourseEntity: The updated course entity.

        Raises:
            CourseNotFoundException: If the course is not found or not owned by company.
        """
        course = await self._repository.get_by_id_and_company(
            course_id=course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=course_id)

        course.status = CourseStatus.PUBLISHED
        course.updated_by = updated_by
        return await self._repository.update(course)
