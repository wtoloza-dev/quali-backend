"""Create training plan use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CreateTrainingPlanUseCase
from .build_training_plan_repository_dependency import TrainingPlanRepositoryDependency


def build_create_training_plan_use_case(
    repository: TrainingPlanRepositoryDependency,
) -> CreateTrainingPlanUseCase:
    """Build a CreateTrainingPlanUseCase with an injected repository.

    Args:
        repository: Training plan repository injected by FastAPI.

    Returns:
        CreateTrainingPlanUseCase: Use case instance ready for execution.
    """
    return CreateTrainingPlanUseCase(repository=repository)


CreateTrainingPlanUseCaseDependency = Annotated[
    CreateTrainingPlanUseCase,
    Depends(build_create_training_plan_use_case),
]
