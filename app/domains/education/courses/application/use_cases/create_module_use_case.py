"""Create module use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import ModuleData, ModuleEntity
from ...domain.exceptions import CourseNotFoundException
from ...domain.ports import CourseRepositoryPort, ModuleRepositoryPort


class CreateModuleUseCase:
    """Add a new module to an existing course.

    Args:
        course_repository: Port to verify the course exists and is owned by the company.
        module_repository: Port to persist the new module.
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
        self, data: ModuleData, company_id: str, created_by: str
    ) -> ModuleEntity:
        """Create and persist a new module.

        Args:
            data: Validated module data from the presentation layer.
            company_id: Owning company — used to verify course ownership.
            created_by: ULID of the user creating the module.

        Returns:
            ModuleEntity: The persisted module entity.

        Raises:
            CourseNotFoundException: If the course does not exist or is not owned by company.
        """
        course = await self._course_repository.get_by_id_and_company(
            course_id=data.course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=data.course_id)

        now = datetime.now(UTC)
        entity = ModuleEntity(
            id=str(ULID()),
            course_id=data.course_id,
            title=data.title,
            order=data.order,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._module_repository.save(entity)
