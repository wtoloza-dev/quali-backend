"""Build list courses use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListCoursesUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_list_courses_use_case(
    repository: CourseRepositoryDependency,
) -> ListCoursesUseCase:
    """Build a ListCoursesUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        ListCoursesUseCase: Use case instance ready for execution.
    """
    return ListCoursesUseCase(repository=repository)


ListCoursesUseCaseDependency = Annotated[
    ListCoursesUseCase,
    Depends(build_list_courses_use_case),
]
