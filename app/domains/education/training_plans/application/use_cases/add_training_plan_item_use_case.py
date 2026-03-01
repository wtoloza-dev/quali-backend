"""Add item to training plan use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import TrainingPlanItemData, TrainingPlanItemEntity
from ...domain.ports import TrainingPlanItemRepositoryPort


class AddTrainingPlanItemUseCase:
    """Add a course item to a training plan."""

    def __init__(self, repository: TrainingPlanItemRepositoryPort) -> None:
        """Initialise with the training plan item repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        data: TrainingPlanItemData,
        created_by: str,
    ) -> TrainingPlanItemEntity:
        """Persist a new training plan item.

        Args:
            data: Item data specifying plan, course, and optional targeting.
            created_by: ULID of the actor adding the item.

        Returns:
            TrainingPlanItemEntity: The persisted item.
        """
        now = datetime.now(UTC)
        entity = TrainingPlanItemEntity(
            id=str(ULID()),
            plan_id=data.plan_id,
            course_id=data.course_id,
            target_role=data.target_role,
            scheduled_date=data.scheduled_date,
            notes=data.notes,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
