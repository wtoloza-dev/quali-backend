"""Build check course access use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CheckCourseAccessUseCase
from .build_course_access_repository_dependency import CourseAccessRepositoryDependency


def build_check_course_access_use_case(
    repository: CourseAccessRepositoryDependency,
) -> CheckCourseAccessUseCase:
    """Build a CheckCourseAccessUseCase with all dependencies injected.

    Args:
        repository: Course access repository injected by FastAPI.

    Returns:
        CheckCourseAccessUseCase: Use case instance ready for execution.
    """
    return CheckCourseAccessUseCase(repository=repository)


CheckCourseAccessUseCaseDependency = Annotated[
    CheckCourseAccessUseCase,
    Depends(build_check_course_access_use_case),
]
