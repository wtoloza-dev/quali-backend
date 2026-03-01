"""Training plan item repository."""

from datetime import UTC, datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import TrainingPlanItemEntity
from ..models.training_plan_item_model import TrainingPlanItemModel


class TrainingPlanItemRepository:
    """Handles all database operations for training plan item entities.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the repository with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: TrainingPlanItemEntity) -> TrainingPlanItemEntity:
        """Persist a new training plan item and return the saved state.

        Args:
            entity: The item entity to persist.

        Returns:
            TrainingPlanItemEntity: The persisted entity.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, item_id: str) -> TrainingPlanItemEntity | None:
        """Retrieve a training plan item by its ULID.

        Args:
            item_id: The ULID of the item.

        Returns:
            TrainingPlanItemEntity if found, None otherwise.
        """
        statement = select(TrainingPlanItemModel).where(
            TrainingPlanItemModel.id == item_id
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def list_by_plan(self, plan_id: str) -> list[TrainingPlanItemEntity]:
        """Return all items for a training plan.

        Args:
            plan_id: The ULID of the training plan.

        Returns:
            List of TrainingPlanItemEntity.
        """
        statement = select(TrainingPlanItemModel).where(
            TrainingPlanItemModel.plan_id == plan_id
        )
        result = await self._session.exec(statement)
        return [self._to_entity(m) for m in result.all()]

    async def delete(self, item_id: str, deleted_by: str) -> None:
        """Hard-delete a training plan item after saving a tombstone.

        Args:
            item_id: The ULID of the item to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        statement = select(TrainingPlanItemModel).where(
            TrainingPlanItemModel.id == item_id
        )
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="training_plan_item",
            entity_id=model.id,
            payload={
                "id": model.id,
                "plan_id": model.plan_id,
                "course_id": model.course_id,
                "target_role": model.target_role,
                "scheduled_date": (
                    model.scheduled_date.isoformat() if model.scheduled_date else None
                ),
                "notes": model.notes,
                "created_by": model.created_by,
            },
            deleted_at=datetime.now(UTC),
            deleted_by=deleted_by,
        )
        self._session.add(tombstone)
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_entity(model: TrainingPlanItemModel) -> TrainingPlanItemEntity:
        """Map a TrainingPlanItemModel ORM instance to a TrainingPlanItemEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            TrainingPlanItemEntity: The domain entity representation.
        """
        return TrainingPlanItemEntity(
            id=model.id,
            plan_id=model.plan_id,
            course_id=model.course_id,
            target_role=model.target_role,
            scheduled_date=model.scheduled_date,
            notes=model.notes,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: TrainingPlanItemEntity) -> TrainingPlanItemModel:
        """Map a TrainingPlanItemEntity to a TrainingPlanItemModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            TrainingPlanItemModel: The ORM model ready for persistence.
        """
        return TrainingPlanItemModel(
            id=entity.id,
            plan_id=entity.plan_id,
            course_id=entity.course_id,
            target_role=entity.target_role,
            scheduled_date=entity.scheduled_date,
            notes=entity.notes,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
