"""Build create lesson use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CreateLessonUseCase
from .build_course_repository_dependency import (
    CourseRepositoryDependency,
)
from .build_lesson_repository_dependency import LessonRepositoryDependency
from .build_module_repository_dependency import ModuleRepositoryDependency


def build_create_lesson_use_case(
    course_repository: CourseRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
    lesson_repository: LessonRepositoryDependency,
) -> CreateLessonUseCase:
    """Build a CreateLessonUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.
        lesson_repository: Lesson repository injected by FastAPI.

    Returns:
        CreateLessonUseCase: Use case instance ready for execution.
    """
    return CreateLessonUseCase(
        course_repository=course_repository,
        module_repository=module_repository,
        lesson_repository=lesson_repository,
    )


CreateLessonUseCaseDependency = Annotated[
    CreateLessonUseCase,
    Depends(build_create_lesson_use_case),
]
