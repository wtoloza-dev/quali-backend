"""Grant course access use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import CourseAccessData, CourseAccessEntity
from ...domain.ports import CourseAccessRepositoryPort


class GrantCourseAccessUseCase:
    """Grant a user access to a course.

    Covers all access types: company enrollment, à la carte purchase,
    and subscription-based access.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseAccessRepositoryPort) -> None:
        """Initialise with the course access repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        data: CourseAccessData,
        created_by: str,
    ) -> CourseAccessEntity:
        """Persist a new course access record.

        Args:
            data: Access data specifying user, course, type, and expiry.
            created_by: ULID of the actor granting access.

        Returns:
            CourseAccessEntity: The persisted access record.
        """
        now = datetime.now(UTC)
        entity = CourseAccessEntity(
            id=str(ULID()),
            user_id=data.user_id,
            course_id=data.course_id,
            access_type=data.access_type,
            expires_at=data.expires_at,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
