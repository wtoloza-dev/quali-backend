"""Delete training plan use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import DeleteTrainingPlanUseCase
from .build_training_plan_repository_dependency import TrainingPlanRepositoryDependency


def build_delete_training_plan_use_case(
    repository: TrainingPlanRepositoryDependency,
) -> DeleteTrainingPlanUseCase:
    """Build a DeleteTrainingPlanUseCase with an injected repository.

    Args:
        repository: Training plan repository injected by FastAPI.

    Returns:
        DeleteTrainingPlanUseCase: Use case instance ready for execution.
    """
    return DeleteTrainingPlanUseCase(repository=repository)


DeleteTrainingPlanUseCaseDependency = Annotated[
    DeleteTrainingPlanUseCase,
    Depends(build_delete_training_plan_use_case),
]
