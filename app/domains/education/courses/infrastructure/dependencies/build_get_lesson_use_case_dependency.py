"""Build get lesson use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetLessonUseCase
from .build_lesson_repository_dependency import LessonRepositoryDependency


def build_get_lesson_use_case(
    repository: LessonRepositoryDependency,
) -> GetLessonUseCase:
    """Build a GetLessonUseCase with all dependencies injected.

    Args:
        repository: Lesson repository injected by FastAPI.

    Returns:
        GetLessonUseCase: Use case instance ready for execution.
    """
    return GetLessonUseCase(repository=repository)


GetLessonUseCaseDependency = Annotated[
    GetLessonUseCase,
    Depends(build_get_lesson_use_case),
]
