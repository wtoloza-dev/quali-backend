"""Create question use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.courses.infrastructure.dependencies import (
    CourseRepositoryDependency,
)

from ...application.use_cases import CreateQuestionUseCase
from .build_question_repository_dependency import QuestionRepositoryDependency


def build_create_question_use_case(
    course_repository: CourseRepositoryDependency,
    repository: QuestionRepositoryDependency,
) -> CreateQuestionUseCase:
    """Build a CreateQuestionUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        repository: Question repository injected by FastAPI.

    Returns:
        CreateQuestionUseCase: Use case instance ready for execution.
    """
    return CreateQuestionUseCase(
        course_repository=course_repository,
        repository=repository,
    )


CreateQuestionUseCaseDependency = Annotated[
    CreateQuestionUseCase,
    Depends(build_create_question_use_case),
]
