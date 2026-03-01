"""Build delete module use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import DeleteModuleUseCase
from .build_course_repository_dependency import CourseRepositoryDependency
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_delete_module_use_case(
    course_repository: CourseRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
) -> DeleteModuleUseCase:
    """Build a DeleteModuleUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.

    Returns:
        DeleteModuleUseCase: Use case instance ready for execution.
    """
    return DeleteModuleUseCase(
        course_repository=course_repository,
        module_repository=module_repository,
    )


DeleteModuleUseCaseDependency = Annotated[
    DeleteModuleUseCase,
    Depends(build_delete_module_use_case),
]
