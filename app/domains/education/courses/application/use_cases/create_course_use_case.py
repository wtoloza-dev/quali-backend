"""Create course use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import CourseData, CourseEntity
from ...domain.ports import CourseRepositoryPort


class CreateCourseUseCase:
    """Handle the creation of a new course.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CourseRepositoryPort) -> None:
        """Initialise with the course repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, data: CourseData, created_by: str) -> CourseEntity:
        """Execute the course creation workflow.

        Args:
            data: Validated course data from the presentation layer.
            created_by: ULID of the authenticated user creating the course.

        Returns:
            CourseEntity: The persisted course entity.
        """
        now = datetime.now(UTC)
        entity = CourseEntity(
            id=str(ULID()),
            company_id=data.company_id,
            title=data.title,
            description=data.description,
            vertical=data.vertical,
            regulatory_ref=data.regulatory_ref,
            validity_days=data.validity_days,
            passing_score=data.passing_score,
            max_attempts=data.max_attempts,
            is_mandatory=data.is_mandatory,
            visibility=data.visibility,
            status=data.status,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
