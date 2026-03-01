"""Build get course use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetCourseUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_get_course_use_case(
    repository: CourseRepositoryDependency,
) -> GetCourseUseCase:
    """Build a GetCourseUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        GetCourseUseCase: Use case instance ready for execution.
    """
    return GetCourseUseCase(repository=repository)


GetCourseUseCaseDependency = Annotated[
    GetCourseUseCase,
    Depends(build_get_course_use_case),
]
