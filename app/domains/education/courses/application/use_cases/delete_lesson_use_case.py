"""Delete lesson use case."""

from ...domain.exceptions import (
    CourseNotFoundException,
    LessonNotFoundException,
    ModuleNotFoundException,
)
from ...domain.ports import (
    CourseRepositoryPort,
    LessonRepositoryPort,
    ModuleRepositoryPort,
)


class DeleteLessonUseCase:
    """Hard-delete a lesson after validating company ownership.

    Args:
        course_repository: Port to verify course ownership.
        module_repository: Port to verify module existence.
        lesson_repository: Port to delete the lesson.
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
        course_id: str,
        company_id: str,
        module_id: str,
        lesson_id: str,
        deleted_by: str,
    ) -> None:
        """Delete the lesson if the company owns the course.

        Args:
            course_id: ULID of the parent course.
            company_id: Owning company — must own the course.
            module_id: ULID of the parent module.
            lesson_id: ULID of the lesson to delete.
            deleted_by: ULID of the user performing the deletion.

        Raises:
            CourseNotFoundException: If the course is not found
                or not owned.
            ModuleNotFoundException: If the module does not exist
                or does not belong to the course.
            LessonNotFoundException: If the lesson does not belong
                to the module.
        """
        course = await self._course_repository.get_by_id_and_company(
            course_id=course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=course_id)

        module = await self._module_repository.get_by_id(module_id)
        if module is None or module.course_id != course_id:
            raise ModuleNotFoundException(module_id=module_id)

        lesson = await self._lesson_repository.get_by_id(lesson_id)
        if lesson is None or lesson.module_id != module_id:
            raise LessonNotFoundException(lesson_id=lesson_id)

        await self._lesson_repository.delete(lesson_id=lesson_id, deleted_by=deleted_by)
