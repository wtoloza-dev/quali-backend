"""Delete training plan use case."""

from ...domain.exceptions import TrainingPlanNotFoundException
from ...domain.ports import TrainingPlanRepositoryPort


class DeleteTrainingPlanUseCase:
    """Remove a training plan."""

    def __init__(self, repository: TrainingPlanRepositoryPort) -> None:
        """Initialise with the training plan repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, plan_id: str, company_id: str, deleted_by: str) -> None:
        """Hard-delete a training plan scoped to a company.

        Args:
            plan_id: ULID of the plan to delete.
            company_id: ULID of the owning company for tenant scoping.
            deleted_by: ULID of the actor performing the deletion.

        Raises:
            TrainingPlanNotFoundException: If no plan with that ID
                exists within the given company.
        """
        entity = await self._repository.get_by_id_and_company(plan_id, company_id)
        if entity is None:
            raise TrainingPlanNotFoundException(plan_id)
        await self._repository.delete(plan_id, deleted_by)
