"""Update module use case."""

from ...domain.entities import ModuleEntity
from ...domain.exceptions import ModuleNotFoundException
from ...domain.ports import ModuleRepositoryPort


class UpdateModuleUseCase:
    """Apply changes to an existing module.

    Receives the full merged entity (Option B).

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: ModuleRepositoryPort) -> None:
        """Initialise with the module repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, entity: ModuleEntity, updated_by: str) -> ModuleEntity:
        """Persist the updated module entity.

        Args:
            entity: Merged module entity with new field values.
            updated_by: ULID of the user performing the update.

        Returns:
            ModuleEntity: The updated entity after persistence.

        Raises:
            ModuleNotFoundException: If the module does not exist.
        """
        existing = await self._repository.get_by_id(entity.id)
        if existing is None:
            raise ModuleNotFoundException(module_id=entity.id)

        entity.updated_by = updated_by
        return await self._repository.update(entity)
