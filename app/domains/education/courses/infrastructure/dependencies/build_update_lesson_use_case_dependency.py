"""Build update lesson use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateLessonUseCase
from .build_lesson_repository_dependency import LessonRepositoryDependency


def build_update_lesson_use_case(
    repository: LessonRepositoryDependency,
) -> UpdateLessonUseCase:
    """Build an UpdateLessonUseCase with all dependencies injected.

    Args:
        repository: Lesson repository injected by FastAPI.

    Returns:
        UpdateLessonUseCase: Use case instance ready for execution.
    """
    return UpdateLessonUseCase(repository=repository)


UpdateLessonUseCaseDependency = Annotated[
    UpdateLessonUseCase,
    Depends(build_update_lesson_use_case),
]
