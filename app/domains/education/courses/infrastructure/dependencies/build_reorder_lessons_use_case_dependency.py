"""Build reorder lessons use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ReorderLessonsUseCase
from .build_course_repository_dependency import (
    CourseRepositoryDependency,
)
from .build_lesson_repository_dependency import LessonRepositoryDependency
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_reorder_lessons_use_case(
    course_repository: CourseRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
    lesson_repository: LessonRepositoryDependency,
) -> ReorderLessonsUseCase:
    """Build a ReorderLessonsUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.
        lesson_repository: Lesson repository injected by FastAPI.

    Returns:
        ReorderLessonsUseCase: Use case instance ready for execution.
    """
    return ReorderLessonsUseCase(
        course_repository=course_repository,
        module_repository=module_repository,
        lesson_repository=lesson_repository,
    )


ReorderLessonsUseCaseDependency = Annotated[
    ReorderLessonsUseCase,
    Depends(build_reorder_lessons_use_case),
]
