"""Build archive course use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ArchiveCourseUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_archive_course_use_case(
    repository: CourseRepositoryDependency,
) -> ArchiveCourseUseCase:
    """Build an ArchiveCourseUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        ArchiveCourseUseCase: Use case instance ready for execution.
    """
    return ArchiveCourseUseCase(repository=repository)


ArchiveCourseUseCaseDependency = Annotated[
    ArchiveCourseUseCase,
    Depends(build_archive_course_use_case),
]
