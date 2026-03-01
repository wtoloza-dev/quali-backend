"""Build create course use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CreateCourseUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_create_course_use_case(
    repository: CourseRepositoryDependency,
) -> CreateCourseUseCase:
    """Build a CreateCourseUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        CreateCourseUseCase: Use case instance ready for execution.
    """
    return CreateCourseUseCase(repository=repository)


CreateCourseUseCaseDependency = Annotated[
    CreateCourseUseCase,
    Depends(build_create_course_use_case),
]
