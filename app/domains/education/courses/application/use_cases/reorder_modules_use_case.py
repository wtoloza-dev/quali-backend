"""Reorder modules use case."""

from ...domain.exceptions import CourseNotFoundException, ModuleNotFoundException
from ...domain.ports import CourseRepositoryPort, ModuleRepositoryPort


class ReorderModulesUseCase:
    """Set new order values for modules within a course.

    Accepts a list of (module_id, order) pairs and applies them atomically.

    Args:
        course_repository: Port to verify course ownership.
        module_repository: Port to update module order fields.
    """

    def __init__(
        self,
        course_repository: CourseRepositoryPort,
        module_repository: ModuleRepositoryPort,
    ) -> None:
        """Initialise with required repositories.

        Args:
            course_repository: Injected course repository.
            module_repository: Injected module repository.
        """
        self._course_repository = course_repository
        self._module_repository = module_repository

    async def execute(
        self,
        course_id: str,
        company_id: str,
        order_map: list[tuple[str, int]],
    ) -> None:
        """Apply new order values to the listed modules.

        Args:
            course_id: ULID of the parent course.
            company_id: Owning company — must own the course.
            order_map: List of (module_id, new_order) pairs.

        Raises:
            CourseNotFoundException: If the course is not found or not owned.
            ModuleNotFoundException: If any module_id does not exist.
        """
        course = await self._course_repository.get_by_id_and_company(
            course_id=course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=course_id)

        for module_id, order in order_map:
            module = await self._module_repository.get_by_id(module_id)
            if module is None or module.course_id != course_id:
                raise ModuleNotFoundException(module_id=module_id)
            await self._module_repository.update_order(module_id=module_id, order=order)
