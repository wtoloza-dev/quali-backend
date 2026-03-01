"""Build update course use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateCourseUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_update_course_use_case(
    repository: CourseRepositoryDependency,
) -> UpdateCourseUseCase:
    """Build an UpdateCourseUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        UpdateCourseUseCase: Use case instance ready for execution.
    """
    return UpdateCourseUseCase(repository=repository)


UpdateCourseUseCaseDependency = Annotated[
    UpdateCourseUseCase,
    Depends(build_update_course_use_case),
]
