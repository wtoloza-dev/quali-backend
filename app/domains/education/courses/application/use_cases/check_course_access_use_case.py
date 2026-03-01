"""Check course access use case."""

from ...domain.ports import CourseAccessRepositoryPort


class CheckCourseAccessUseCase:
    """Determine whether a user has active access to a course.

    Used by routes to decide whether to return full lesson content
    or a locked placeholder.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseAccessRepositoryPort) -> None:
        """Initialise with the course access repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, user_id: str, course_id: str) -> bool:
        """Return True if the user has active (non-expired) access to the course.

        Args:
            user_id: ULID of the user.
            course_id: ULID of the course.

        Returns:
            bool: True if active access exists, False otherwise.
        """
        access = await self._repository.get_active_access(
            user_id=user_id,
            course_id=course_id,
        )
        return access is not None
