"""Create lesson use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import LessonData, LessonEntity
from ...domain.exceptions import (
    CourseNotFoundException,
    ModuleNotFoundException,
)
from ...domain.ports import (
    CourseRepositoryPort,
    LessonRepositoryPort,
    ModuleRepositoryPort,
)


class CreateLessonUseCase:
    """Add a new lesson to an existing module.

    Args:
        course_repository: Port to verify course ownership.
        module_repository: Port to verify the module exists.
        lesson_repository: Port to persist the new lesson.
    """

    def __init__(
        self,
        course_repository: CourseRepositoryPort,
        module_repository: ModuleRepositoryPort,
        lesson_repository: LessonRepositoryPort,
    ) -> None:
        """Initialise with required repositories.

        Args:
            course_repository: Injected course repository.
            module_repository: Injected module repository.
            lesson_repository: Injected lesson repository.
        """
        self._course_repository = course_repository
        self._module_repository = module_repository
        self._lesson_repository = lesson_repository

    async def execute(
        self,
        data: LessonData,
        company_id: str,
        created_by: str,
    ) -> LessonEntity:
        """Create and persist a new lesson.

        Args:
            data: Validated lesson data from the presentation layer.
            company_id: Owning company — used to verify course
                ownership.
            created_by: ULID of the user creating the lesson.

        Returns:
            LessonEntity: The persisted lesson entity.

        Raises:
            ModuleNotFoundException: If the module does not exist.
            CourseNotFoundException: If the course is not found
                or not owned by the company.
        """
        module = await self._module_repository.get_by_id(data.module_id)
        if module is None:
            raise ModuleNotFoundException(module_id=data.module_id)

        course = await self._course_repository.get_by_id_and_company(
            course_id=module.course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=module.course_id)

        now = datetime.now(UTC)
        entity = LessonEntity(
            id=str(ULID()),
            module_id=data.module_id,
            title=data.title,
            content=data.content,
            order=data.order,
            is_preview=data.is_preview,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._lesson_repository.save(entity)
