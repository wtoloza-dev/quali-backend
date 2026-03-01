"""Build list lessons use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListLessonsUseCase
from .build_lesson_repository_dependency import LessonRepositoryDependency


def build_list_lessons_use_case(
    repository: LessonRepositoryDependency,
) -> ListLessonsUseCase:
    """Build a ListLessonsUseCase with all dependencies injected.

    Args:
        repository: Lesson repository injected by FastAPI.

    Returns:
        ListLessonsUseCase: Use case instance ready for execution.
    """
    return ListLessonsUseCase(repository=repository)


ListLessonsUseCaseDependency = Annotated[
    ListLessonsUseCase,
    Depends(build_list_lessons_use_case),
]
