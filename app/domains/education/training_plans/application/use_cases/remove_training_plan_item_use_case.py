"""Remove item from training plan use case."""

from ...domain.exceptions import TrainingPlanItemNotFoundException
from ...domain.ports import TrainingPlanItemRepositoryPort


class RemoveTrainingPlanItemUseCase:
    """Remove an item from a training plan."""

    def __init__(self, repository: TrainingPlanItemRepositoryPort) -> None:
        """Initialise with the training plan item repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, item_id: str, deleted_by: str) -> None:
        """Hard-delete a training plan item.

        Args:
            item_id: ULID of the item to remove.
            deleted_by: ULID of the actor performing the deletion.

        Raises:
            TrainingPlanItemNotFoundException: If no item with that ID exists.
        """
        entity = await self._repository.get_by_id(item_id)
        if entity is None:
            raise TrainingPlanItemNotFoundException(item_id)
        await self._repository.delete(item_id, deleted_by)
