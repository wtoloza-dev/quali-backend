"""Update training plan use case."""

from ...domain.entities import TrainingPlanEntity
from ...domain.ports import TrainingPlanRepositoryPort


class UpdateTrainingPlanUseCase:
    """Persist changes to an existing training plan.

    Follows Option B: caller merges patch into the full entity and passes it here.
    """

    def __init__(self, repository: TrainingPlanRepositoryPort) -> None:
        """Initialise with the training plan repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, entity: TrainingPlanEntity) -> TrainingPlanEntity:
        """Persist the updated training plan.

        Args:
            entity: The full training plan entity with updated fields.

        Returns:
            TrainingPlanEntity: The updated entity after persistence.
        """
        return await self._repository.update(entity)
