"""Reorder lessons use case."""

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


class ReorderLessonsUseCase:
    """Set new order values for lessons within a module.

    Args:
        course_repository: Port to verify course ownership.
        module_repository: Port to verify the module exists.
        lesson_repository: Port to update lesson order fields.
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
        order_map: list[tuple[str, int]],
    ) -> None:
        """Apply new order values to the listed lessons.

        Args:
            course_id: ULID of the parent course.
            company_id: Owning company — must own the course.
            module_id: ULID of the parent module.
            order_map: List of (lesson_id, new_order) pairs.

        Raises:
            CourseNotFoundException: If the course is not found
                or not owned.
            ModuleNotFoundException: If the module does not exist
                or does not belong to the course.
            LessonNotFoundException: If any lesson_id does not
                belong to the module.
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

        for lesson_id, order in order_map:
            lesson = await self._lesson_repository.get_by_id(lesson_id)
            if lesson is None or lesson.module_id != module_id:
                raise LessonNotFoundException(lesson_id=lesson_id)
            await self._lesson_repository.update_order(lesson_id=lesson_id, order=order)
