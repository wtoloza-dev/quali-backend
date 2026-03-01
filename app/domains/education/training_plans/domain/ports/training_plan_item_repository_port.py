"""Training plan item repository port."""

from typing import Protocol

from ..entities import TrainingPlanItemEntity


class TrainingPlanItemRepositoryPort(Protocol):
    """Interface for the training plan item repository."""

    async def save(self, entity: TrainingPlanItemEntity) -> TrainingPlanItemEntity:
        """Persist a new training plan item and return it."""
        ...

    async def get_by_id(self, item_id: str) -> TrainingPlanItemEntity | None:
        """Return a training plan item by ID, or None if not found."""
        ...

    async def list_by_plan(self, plan_id: str) -> list[TrainingPlanItemEntity]:
        """Return all items belonging to a training plan."""
        ...

    async def delete(self, item_id: str, deleted_by: str) -> None:
        """Hard-delete a training plan item after saving a tombstone.

        Args:
            item_id: The ULID of the item to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        ...
