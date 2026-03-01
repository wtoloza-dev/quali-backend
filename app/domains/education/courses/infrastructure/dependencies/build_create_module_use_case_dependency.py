"""Build create module use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CreateModuleUseCase
from .build_course_repository_dependency import CourseRepositoryDependency
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_create_module_use_case(
    course_repository: CourseRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
) -> CreateModuleUseCase:
    """Build a CreateModuleUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.

    Returns:
        CreateModuleUseCase: Use case instance ready for execution.
    """
    return CreateModuleUseCase(
        course_repository=course_repository,
        module_repository=module_repository,
    )


CreateModuleUseCaseDependency = Annotated[
    CreateModuleUseCase,
    Depends(build_create_module_use_case),
]
