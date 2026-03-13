"""ListAllCoursesUseCase dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListAllCoursesUseCase
from .build_course_repository_dependency import CourseRepositoryDependency


def build_list_all_courses_use_case(
    repository: CourseRepositoryDependency,
) -> ListAllCoursesUseCase:
    """Build a ListAllCoursesUseCase with all dependencies injected.

    Args:
        repository: Course repository injected by FastAPI.

    Returns:
        ListAllCoursesUseCase: Use case instance ready for execution.
    """
    return ListAllCoursesUseCase(repository=repository)


ListAllCoursesUseCaseDependency = Annotated[
    ListAllCoursesUseCase,
    Depends(build_list_all_courses_use_case),
]
