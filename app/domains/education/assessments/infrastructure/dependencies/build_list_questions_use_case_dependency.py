"""List questions use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.courses.infrastructure.dependencies import (
    CourseRepositoryDependency,
)

from ...application.use_cases import ListQuestionsUseCase
from .build_question_repository_dependency import QuestionRepositoryDependency


def build_list_questions_use_case(
    course_repository: CourseRepositoryDependency,
    repository: QuestionRepositoryDependency,
) -> ListQuestionsUseCase:
    """Build a ListQuestionsUseCase with all dependencies injected.

    Args:
        course_repository: Course repository injected by FastAPI.
        repository: Question repository injected by FastAPI.

    Returns:
        ListQuestionsUseCase: Use case instance ready for execution.
    """
    return ListQuestionsUseCase(
        course_repository=course_repository,
        repository=repository,
    )


ListQuestionsUseCaseDependency = Annotated[
    ListQuestionsUseCase,
    Depends(build_list_questions_use_case),
]
