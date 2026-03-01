"""Build delete lesson use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import DeleteLessonUseCase
from .build_course_repository_dependency import (
    CourseRepositoryDependency,
)
from .build_lesson_repository_dependency import LessonRepositoryDependency
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_delete_lesson_use_case(
    course_repository: CourseRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
    lesson_repository: LessonRepositoryDependency,
) -> DeleteLessonUseCase:
    """Build a DeleteLessonUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.
        lesson_repository: Lesson repository injected by FastAPI.

    Returns:
        DeleteLessonUseCase: Use case instance ready for execution.
    """
    return DeleteLessonUseCase(
        course_repository=course_repository,
        module_repository=module_repository,
        lesson_repository=lesson_repository,
    )


DeleteLessonUseCaseDependency = Annotated[
    DeleteLessonUseCase,
    Depends(build_delete_lesson_use_case),
]
