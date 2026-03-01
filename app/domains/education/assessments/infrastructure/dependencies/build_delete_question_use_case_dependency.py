"""Delete question use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.courses.infrastructure.dependencies import (
    CourseRepositoryDependency,
)

from ...application.use_cases import DeleteQuestionUseCase
from .build_question_repository_dependency import QuestionRepositoryDependency


def build_delete_question_use_case(
    course_repository: CourseRepositoryDependency,
    repository: QuestionRepositoryDependency,
) -> DeleteQuestionUseCase:
    """Build a DeleteQuestionUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        repository: Question repository injected by FastAPI.

    Returns:
        DeleteQuestionUseCase: Use case instance ready for execution.
    """
    return DeleteQuestionUseCase(
        course_repository=course_repository,
        repository=repository,
    )


DeleteQuestionUseCaseDependency = Annotated[
    DeleteQuestionUseCase,
    Depends(build_delete_question_use_case),
]
