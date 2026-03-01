"""Training plans subdomain dependency factories."""

from .build_add_training_plan_item_use_case_dependency import (
    AddTrainingPlanItemUseCaseDependency,
)
from .build_create_training_plan_use_case_dependency import (
    CreateTrainingPlanUseCaseDependency,
)
from .build_delete_training_plan_use_case_dependency import (
    DeleteTrainingPlanUseCaseDependency,
)
from .build_get_training_plan_use_case_dependency import (
    GetTrainingPlanUseCaseDependency,
)
from .build_list_training_plans_use_case_dependency import (
    ListTrainingPlansUseCaseDependency,
)
from .build_remove_training_plan_item_use_case_dependency import (
    RemoveTrainingPlanItemUseCaseDependency,
)
from .build_training_plan_item_repository_dependency import (
    TrainingPlanItemRepositoryDependency,
)
from .build_training_plan_repository_dependency import TrainingPlanRepositoryDependency
from .build_update_training_plan_use_case_dependency import (
    UpdateTrainingPlanUseCaseDependency,
)


__all__ = [
    "TrainingPlanRepositoryDependency",
    "TrainingPlanItemRepositoryDependency",
    "CreateTrainingPlanUseCaseDependency",
    "GetTrainingPlanUseCaseDependency",
    "ListTrainingPlansUseCaseDependency",
    "UpdateTrainingPlanUseCaseDependency",
    "DeleteTrainingPlanUseCaseDependency",
    "AddTrainingPlanItemUseCaseDependency",
    "RemoveTrainingPlanItemUseCaseDependency",
]
