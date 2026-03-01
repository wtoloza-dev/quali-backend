"""Create training plan use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import TrainingPlanData, TrainingPlanEntity
from ...domain.enums import TrainingPlanStatus
from ...domain.ports import TrainingPlanRepositoryPort


class CreateTrainingPlanUseCase:
    """Create a new annual training plan for a company."""

    def __init__(self, repository: TrainingPlanRepositoryPort) -> None:
        """Initialise with the training plan repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        data: TrainingPlanData,
        created_by: str,
    ) -> TrainingPlanEntity:
        """Persist a new training plan.

        Args:
            data: Plan data specifying company, year, and title.
            created_by: ULID of the actor creating the plan.

        Returns:
            TrainingPlanEntity: The persisted training plan.
        """
        now = datetime.now(UTC)
        entity = TrainingPlanEntity(
            id=str(ULID()),
            company_id=data.company_id,
            year=data.year,
            title=data.title,
            status=TrainingPlanStatus.DRAFT,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
