"""Build list modules use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListModulesUseCase
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_list_modules_use_case(
    repository: ModuleRepositoryDependency,
) -> ListModulesUseCase:
    """Build a ListModulesUseCase with all dependencies injected.

    Args:
        repository: Module repository injected by FastAPI.

    Returns:
        ListModulesUseCase: Use case instance ready for execution.
    """
    return ListModulesUseCase(repository=repository)


ListModulesUseCaseDependency = Annotated[
    ListModulesUseCase,
    Depends(build_list_modules_use_case),
]
