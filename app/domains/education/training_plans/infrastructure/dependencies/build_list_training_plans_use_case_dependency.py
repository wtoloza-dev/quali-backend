"""List training plans use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListTrainingPlansUseCase
from .build_training_plan_repository_dependency import TrainingPlanRepositoryDependency


def build_list_training_plans_use_case(
    repository: TrainingPlanRepositoryDependency,
) -> ListTrainingPlansUseCase:
    """Build a ListTrainingPlansUseCase with an injected repository.

    Args:
        repository: Training plan repository injected by FastAPI.

    Returns:
        ListTrainingPlansUseCase: Use case instance ready for execution.
    """
    return ListTrainingPlansUseCase(repository=repository)


ListTrainingPlansUseCaseDependency = Annotated[
    ListTrainingPlansUseCase,
    Depends(build_list_training_plans_use_case),
]
