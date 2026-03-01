"""Get training plan use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetTrainingPlanUseCase
from .build_training_plan_repository_dependency import TrainingPlanRepositoryDependency


def build_get_training_plan_use_case(
    repository: TrainingPlanRepositoryDependency,
) -> GetTrainingPlanUseCase:
    """Build a GetTrainingPlanUseCase with an injected repository.

    Args:
        repository: Training plan repository injected by FastAPI.

    Returns:
        GetTrainingPlanUseCase: Use case instance ready for execution.
    """
    return GetTrainingPlanUseCase(repository=repository)


GetTrainingPlanUseCaseDependency = Annotated[
    GetTrainingPlanUseCase,
    Depends(build_get_training_plan_use_case),
]
