"""Remove training plan item use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import RemoveTrainingPlanItemUseCase
from .build_training_plan_item_repository_dependency import (
    TrainingPlanItemRepositoryDependency,
)


def build_remove_training_plan_item_use_case(
    repository: TrainingPlanItemRepositoryDependency,
) -> RemoveTrainingPlanItemUseCase:
    """Build a RemoveTrainingPlanItemUseCase with an injected repository.

    Args:
        repository: Training plan item repository injected by FastAPI.

    Returns:
        RemoveTrainingPlanItemUseCase: Use case instance ready for execution.
    """
    return RemoveTrainingPlanItemUseCase(repository=repository)


RemoveTrainingPlanItemUseCaseDependency = Annotated[
    RemoveTrainingPlanItemUseCase,
    Depends(build_remove_training_plan_item_use_case),
]
