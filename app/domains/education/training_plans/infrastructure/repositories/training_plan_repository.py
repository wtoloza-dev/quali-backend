"""Training plan repository."""

from datetime import UTC, datetime

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import TrainingPlanEntity
from ...domain.enums import TrainingPlanStatus
from ..models.training_plan_model import TrainingPlanModel


class TrainingPlanRepository:
    """Handles all database operations for training plan entities.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the repository with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: TrainingPlanEntity) -> TrainingPlanEntity:
        """Persist a new training plan and return the saved state.

        Args:
            entity: The training plan entity to persist.

        Returns:
            TrainingPlanEntity: The persisted entity.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, plan_id: str) -> TrainingPlanEntity | None:
        """Retrieve a training plan by its ULID.

        Args:
            plan_id: The ULID of the training plan.

        Returns:
            TrainingPlanEntity if found, None otherwise.
        """
        statement = select(TrainingPlanModel).where(TrainingPlanModel.id == plan_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_id_and_company(
        self, plan_id: str, company_id: str
    ) -> TrainingPlanEntity | None:
        """Retrieve a training plan scoped to a specific company.

        Returns None if the plan does not exist or belongs to a
        different company, preventing cross-tenant data access.

        Args:
            plan_id: The ULID of the training plan.
            company_id: The ULID of the owning company.

        Returns:
            TrainingPlanEntity if found within the company,
            None otherwise.
        """
        statement = select(TrainingPlanModel).where(
            TrainingPlanModel.id == plan_id,
            TrainingPlanModel.company_id == company_id,
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def update(self, entity: TrainingPlanEntity) -> TrainingPlanEntity:
        """Persist changes to an existing training plan.

        Args:
            entity: The training plan entity with updated fields.

        Returns:
            TrainingPlanEntity: The updated entity after persistence.
        """
        statement = select(TrainingPlanModel).where(TrainingPlanModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.title = entity.title
        model.status = entity.status
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, plan_id: str, deleted_by: str) -> None:
        """Hard-delete a training plan and archive a tombstone snapshot.

        Args:
            plan_id: The ULID of the plan to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        statement = select(TrainingPlanModel).where(TrainingPlanModel.id == plan_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="training_plan",
            entity_id=model.id,
            payload={
                "id": model.id,
                "company_id": model.company_id,
                "year": model.year,
                "title": model.title,
                "status": model.status,
                "created_by": model.created_by,
            },
            deleted_at=datetime.now(UTC),
            deleted_by=deleted_by,
        )
        self._session.add(tombstone)
        await self._session.delete(model)
        await self._session.flush()

    async def list_by_company(
        self,
        company_id: str,
        page: int,
        page_size: int,
    ) -> tuple[list[TrainingPlanEntity], int]:
        """Return a paginated slice of training plans for a company.

        Args:
            company_id: ULID of the company to scope the listing.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of TrainingPlanEntity, total count).
        """
        count_stmt = (
            select(func.count())
            .select_from(TrainingPlanModel)
            .where(TrainingPlanModel.company_id == company_id)
        )
        total = (await self._session.exec(count_stmt)).one()

        stmt = (
            select(TrainingPlanModel)
            .where(TrainingPlanModel.company_id == company_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        models = (await self._session.exec(stmt)).all()
        return [self._to_entity(m) for m in models], total

    @staticmethod
    def _to_entity(model: TrainingPlanModel) -> TrainingPlanEntity:
        """Map a TrainingPlanModel ORM instance to a TrainingPlanEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            TrainingPlanEntity: The domain entity representation.
        """
        return TrainingPlanEntity(
            id=model.id,
            company_id=model.company_id,
            year=model.year,
            title=model.title,
            status=TrainingPlanStatus(model.status),
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: TrainingPlanEntity) -> TrainingPlanModel:
        """Map a TrainingPlanEntity to a TrainingPlanModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            TrainingPlanModel: The ORM model ready for persistence.
        """
        return TrainingPlanModel(
            id=entity.id,
            company_id=entity.company_id,
            year=entity.year,
            title=entity.title,
            status=entity.status,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
