"""Add training plan item use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import AddTrainingPlanItemUseCase
from .build_training_plan_item_repository_dependency import (
    TrainingPlanItemRepositoryDependency,
)


def build_add_training_plan_item_use_case(
    repository: TrainingPlanItemRepositoryDependency,
) -> AddTrainingPlanItemUseCase:
    """Build an AddTrainingPlanItemUseCase with an injected repository.

    Args:
        repository: Training plan item repository injected by FastAPI.

    Returns:
        AddTrainingPlanItemUseCase: Use case instance ready for execution.
    """
    return AddTrainingPlanItemUseCase(repository=repository)


AddTrainingPlanItemUseCaseDependency = Annotated[
    AddTrainingPlanItemUseCase,
    Depends(build_add_training_plan_item_use_case),
]
