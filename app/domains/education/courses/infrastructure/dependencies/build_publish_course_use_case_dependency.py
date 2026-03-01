"""Build publish course use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import PublishCourseUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_publish_course_use_case(
    repository: CourseRepositoryDependency,
) -> PublishCourseUseCase:
    """Build a PublishCourseUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        PublishCourseUseCase: Use case instance ready for execution.
    """
    return PublishCourseUseCase(repository=repository)


PublishCourseUseCaseDependency = Annotated[
    PublishCourseUseCase,
    Depends(build_publish_course_use_case),
]
