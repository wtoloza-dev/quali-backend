"""Build delete course use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import DeleteCourseUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_delete_course_use_case(
    repository: CourseRepositoryDependency,
) -> DeleteCourseUseCase:
    """Build a DeleteCourseUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        DeleteCourseUseCase: Use case instance ready for execution.
    """
    return DeleteCourseUseCase(repository=repository)


DeleteCourseUseCaseDependency = Annotated[
    DeleteCourseUseCase,
    Depends(build_delete_course_use_case),
]
