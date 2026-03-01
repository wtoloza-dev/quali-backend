"""Get training plan use case."""

from ...domain.entities import TrainingPlanEntity
from ...domain.exceptions import TrainingPlanNotFoundException
from ...domain.ports import TrainingPlanRepositoryPort


class GetTrainingPlanUseCase:
    """Retrieve a single training plan by its ULID."""

    def __init__(self, repository: TrainingPlanRepositoryPort) -> None:
        """Initialise with the training plan repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, plan_id: str, company_id: str) -> TrainingPlanEntity:
        """Retrieve a training plan scoped to a company.

        Args:
            plan_id: ULID of the training plan to retrieve.
            company_id: ULID of the owning company for tenant scoping.

        Returns:
            TrainingPlanEntity: The matching plan.

        Raises:
            TrainingPlanNotFoundException: If no plan with that ID
                exists within the given company.
        """
        entity = await self._repository.get_by_id_and_company(plan_id, company_id)
        if entity is None:
            raise TrainingPlanNotFoundException(plan_id)
        return entity
