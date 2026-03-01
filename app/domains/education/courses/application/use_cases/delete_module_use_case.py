"""Delete module use case."""

from ...domain.exceptions import CourseNotFoundException, ModuleNotFoundException
from ...domain.ports import CourseRepositoryPort, ModuleRepositoryPort


class DeleteModuleUseCase:
    """Hard-delete a module and all its lessons.

    Args:
        course_repository: Port to verify course ownership.
        module_repository: Port to delete the module.
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
        module_id: str,
        company_id: str,
        deleted_by: str,
    ) -> None:
        """Delete the module if the company owns the parent course.

        Args:
            course_id: ULID of the parent course.
            module_id: ULID of the module to delete.
            company_id: Owning company — must own the course.
            deleted_by: ULID of the user performing the deletion.

        Raises:
            CourseNotFoundException: If the course is not found or not owned.
            ModuleNotFoundException: If the module does not belong to the course.
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

        await self._module_repository.delete(module_id=module_id, deleted_by=deleted_by)
