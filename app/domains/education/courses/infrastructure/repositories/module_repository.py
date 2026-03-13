"""Module repository."""

from datetime import UTC, datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import ModuleEntity
from ..models.module_model import ModuleModel


class ModuleRepository:
    """Handles all database operations for module entities.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: ModuleEntity) -> ModuleEntity:
        """Persist a new module and return the saved state.

        Args:
            entity: The module entity to persist.

        Returns:
            ModuleEntity: The persisted entity.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, module_id: str) -> ModuleEntity | None:
        """Retrieve a module by ULID.

        Args:
            module_id: The ULID of the module.

        Returns:
            ModuleEntity if found, None otherwise.
        """
        statement = select(ModuleModel).where(ModuleModel.id == module_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def list_by_course(self, course_id: str) -> list[ModuleEntity]:
        """Return all modules for a course ordered by their order field.

        Args:
            course_id: The ULID of the parent course.

        Returns:
            List of ModuleEntity sorted ascending by order.
        """
        statement = (
            select(ModuleModel)
            .where(ModuleModel.course_id == course_id)
            .order_by(ModuleModel.order)
        )
        result = await self._session.exec(statement)
        return [self._to_entity(m) for m in result.all()]

    async def update(self, entity: ModuleEntity) -> ModuleEntity:
        """Persist changes to an existing module entity.

        Args:
            entity: The module entity with updated fields.

        Returns:
            ModuleEntity: The updated entity after persistence.
        """
        statement = select(ModuleModel).where(ModuleModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.title = entity.title
        model.order = entity.order
        model.passing_score = entity.passing_score
        model.max_attempts = entity.max_attempts
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, module_id: str, deleted_by: str) -> None:
        """Hard-delete a module and archive a tombstone snapshot.

        Cascade deletes lessons via DB FK constraint.

        Args:
            module_id: The ULID of the module to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        statement = select(ModuleModel).where(ModuleModel.id == module_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="module",
            entity_id=model.id,
            payload={
                "id": model.id,
                "course_id": model.course_id,
                "title": model.title,
                "order": model.order,
                "passing_score": model.passing_score,
                "max_attempts": model.max_attempts,
                "created_at": model.created_at.isoformat()
                if model.created_at
                else None,
                "created_by": model.created_by,
            },
            deleted_at=datetime.now(UTC),
            deleted_by=deleted_by,
        )
        self._session.add(tombstone)
        await self._session.delete(model)
        await self._session.flush()

    async def update_order(self, module_id: str, order: int) -> None:
        """Update only the order field of a module.

        Args:
            module_id: The ULID of the module.
            order: The new order value.
        """
        statement = select(ModuleModel).where(ModuleModel.id == module_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return
        model.order = order
        self._session.add(model)
        await self._session.flush()

    @staticmethod
    def _to_entity(model: ModuleModel) -> ModuleEntity:
        """Map a ModuleModel to a ModuleEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            ModuleEntity: The domain entity representation.
        """
        return ModuleEntity(
            id=model.id,
            course_id=model.course_id,
            title=model.title,
            order=model.order,
            passing_score=model.passing_score,
            max_attempts=model.max_attempts,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: ModuleEntity) -> ModuleModel:
        """Map a ModuleEntity to a ModuleModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            ModuleModel: The ORM model ready for persistence.
        """
        return ModuleModel(
            id=entity.id,
            course_id=entity.course_id,
            title=entity.title,
            order=entity.order,
            passing_score=entity.passing_score,
            max_attempts=entity.max_attempts,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
