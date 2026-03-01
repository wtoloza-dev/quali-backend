"""Module repository port."""

from typing import Protocol

from ..entities import ModuleEntity


class ModuleRepositoryPort(Protocol):
    """Interface for the module repository."""

    async def save(self, entity: ModuleEntity) -> ModuleEntity:
        """Persist a new module and return the saved state.

        Args:
            entity: The module entity to persist.

        Returns:
            ModuleEntity: The persisted entity.
        """
        ...

    async def get_by_id(self, module_id: str) -> ModuleEntity | None:
        """Retrieve a module by ULID.

        Args:
            module_id: The ULID of the module.

        Returns:
            ModuleEntity if found, None otherwise.
        """
        ...

    async def list_by_course(self, course_id: str) -> list[ModuleEntity]:
        """Return all modules for a course ordered by their order field.

        Args:
            course_id: The ULID of the parent course.

        Returns:
            List of ModuleEntity sorted by order ascending.
        """
        ...

    async def update(self, entity: ModuleEntity) -> ModuleEntity:
        """Persist changes to an existing module entity.

        Args:
            entity: The module entity with updated fields.

        Returns:
            ModuleEntity: The updated entity after persistence.
        """
        ...

    async def delete(self, module_id: str, deleted_by: str) -> None:
        """Hard-delete a module and all its lessons.

        Args:
            module_id: The ULID of the module to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        ...

    async def update_order(self, module_id: str, order: int) -> None:
        """Update only the order field of a module.

        Args:
            module_id: The ULID of the module.
            order: The new order value.
        """
        ...
