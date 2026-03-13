"""Build update module use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateModuleUseCase
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_update_module_use_case(
    repository: ModuleRepositoryDependency,
) -> UpdateModuleUseCase:
    """Build an UpdateModuleUseCase with all dependencies injected.

    Args:
        repository: Module repository injected by FastAPI.

    Returns:
        UpdateModuleUseCase: Use case instance ready for execution.
    """
    return UpdateModuleUseCase(repository=repository)


UpdateModuleUseCaseDependency = Annotated[
    UpdateModuleUseCase,
    Depends(build_update_module_use_case),
]
