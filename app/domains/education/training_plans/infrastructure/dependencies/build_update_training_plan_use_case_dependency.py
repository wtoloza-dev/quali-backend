"""Update training plan use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateTrainingPlanUseCase
from .build_training_plan_repository_dependency import TrainingPlanRepositoryDependency


def build_update_training_plan_use_case(
    repository: TrainingPlanRepositoryDependency,
) -> UpdateTrainingPlanUseCase:
    """Build an UpdateTrainingPlanUseCase with an injected repository.

    Args:
        repository: Training plan repository injected by FastAPI.

    Returns:
        UpdateTrainingPlanUseCase: Use case instance ready for execution.
    """
    return UpdateTrainingPlanUseCase(repository=repository)


UpdateTrainingPlanUseCaseDependency = Annotated[
    UpdateTrainingPlanUseCase,
    Depends(build_update_training_plan_use_case),
]
