"""Build grant course access use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GrantCourseAccessUseCase
from .build_course_access_repository_dependency import CourseAccessRepositoryDependency


def build_grant_course_access_use_case(
    repository: CourseAccessRepositoryDependency,
) -> GrantCourseAccessUseCase:
    """Build a GrantCourseAccessUseCase with all dependencies injected.

    Args:
        repository: Course access repository injected by FastAPI.

    Returns:
        GrantCourseAccessUseCase: Use case instance ready for execution.
    """
    return GrantCourseAccessUseCase(repository=repository)


GrantCourseAccessUseCaseDependency = Annotated[
    GrantCourseAccessUseCase,
    Depends(build_grant_course_access_use_case),
]
