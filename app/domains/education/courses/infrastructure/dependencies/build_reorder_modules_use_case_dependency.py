"""Build reorder modules use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ReorderModulesUseCase
from .build_course_repository_dependency import CourseRepositoryDependency
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_reorder_modules_use_case(
    course_repository: CourseRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
) -> ReorderModulesUseCase:
    """Build a ReorderModulesUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.

    Returns:
        ReorderModulesUseCase: Use case instance ready for execution.
    """
    return ReorderModulesUseCase(
        course_repository=course_repository,
        module_repository=module_repository,
    )


ReorderModulesUseCaseDependency = Annotated[
    ReorderModulesUseCase,
    Depends(build_reorder_modules_use_case),
]
