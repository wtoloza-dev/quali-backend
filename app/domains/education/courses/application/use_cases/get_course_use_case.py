"""Get course use case."""

from ...domain.entities import CourseEntity
from ...domain.exceptions import CourseNotFoundException
from ...domain.ports import CourseRepositoryPort


class GetCourseUseCase:
    """Retrieve a single course visible to the requesting company.

    Public courses are accessible by any company.
    Private courses are only accessible by the owning company.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseRepositoryPort) -> None:
        """Initialise with the course repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, course_id: str, company_id: str) -> CourseEntity:
        """Return the course if visible to the requesting company.

        Args:
            course_id: ULID of the course to retrieve.
            company_id: ID of the company making the request.

        Returns:
            CourseEntity: The found course.

        Raises:
            CourseNotFoundException: If the course does not exist or is not visible.
        """
        course = await self._repository.get_by_id(course_id)
        if course is None:
            raise CourseNotFoundException(course_id=course_id)

        from ...domain.enums import CourseVisibility

        if (
            course.visibility == CourseVisibility.PRIVATE
            and course.company_id != company_id
        ):
            raise CourseNotFoundException(course_id=course_id)

        return course
