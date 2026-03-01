"""Lesson repository."""

from datetime import UTC, datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import ContentBlock, LessonEntity
from ..models.lesson_model import LessonModel


class LessonRepository:
    """Handles all database operations for lesson entities.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: LessonEntity) -> LessonEntity:
        """Persist a new lesson and return the saved state.

        Args:
            entity: The lesson entity to persist.

        Returns:
            LessonEntity: The persisted entity.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, lesson_id: str) -> LessonEntity | None:
        """Retrieve a lesson by ULID.

        Args:
            lesson_id: The ULID of the lesson.

        Returns:
            LessonEntity if found, None otherwise.
        """
        statement = select(LessonModel).where(LessonModel.id == lesson_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def list_by_module(self, module_id: str) -> list[LessonEntity]:
        """Return all lessons for a module ordered by their order field.

        Args:
            module_id: The ULID of the parent module.

        Returns:
            List of LessonEntity sorted ascending by order.
        """
        statement = (
            select(LessonModel)
            .where(LessonModel.module_id == module_id)
            .order_by(LessonModel.order)
        )
        result = await self._session.exec(statement)
        return [self._to_entity(m) for m in result.all()]

    async def update(self, entity: LessonEntity) -> LessonEntity:
        """Persist changes to an existing lesson entity.

        Args:
            entity: The lesson entity with updated fields.

        Returns:
            LessonEntity: The updated entity after persistence.
        """
        statement = select(LessonModel).where(LessonModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.title = entity.title
        model.content = [block.model_dump() for block in entity.content]
        model.order = entity.order
        model.is_preview = entity.is_preview
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, lesson_id: str, deleted_by: str) -> None:
        """Hard-delete a lesson and archive a tombstone snapshot.

        Args:
            lesson_id: The ULID of the lesson to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        statement = select(LessonModel).where(LessonModel.id == lesson_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="lesson",
            entity_id=model.id,
            payload={
                "id": model.id,
                "module_id": model.module_id,
                "title": model.title,
                "order": model.order,
                "is_preview": model.is_preview,
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

    async def update_order(self, lesson_id: str, order: int) -> None:
        """Update only the order field of a lesson.

        Args:
            lesson_id: The ULID of the lesson.
            order: The new order value.
        """
        statement = select(LessonModel).where(LessonModel.id == lesson_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return
        model.order = order
        self._session.add(model)
        await self._session.flush()

    @staticmethod
    def _to_entity(model: LessonModel) -> LessonEntity:
        """Map a LessonModel to a LessonEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            LessonEntity: The domain entity representation.
        """
        return LessonEntity(
            id=model.id,
            module_id=model.module_id,
            title=model.title,
            content=[
                ContentBlock.model_validate(block) for block in (model.content or [])
            ],
            order=model.order,
            is_preview=model.is_preview,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: LessonEntity) -> LessonModel:
        """Map a LessonEntity to a LessonModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            LessonModel: The ORM model ready for persistence.
        """
        return LessonModel(
            id=entity.id,
            module_id=entity.module_id,
            title=entity.title,
            content=[block.model_dump() for block in entity.content],
            order=entity.order,
            is_preview=entity.is_preview,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
