"""Submit attempt use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.courses.infrastructure.dependencies import (
    ModuleRepositoryDependency,
)
from app.domains.education.enrollments.infrastructure.dependencies import (
    EnrollmentRepositoryDependency,
)

from ...application.use_cases import SubmitAttemptUseCase
from .build_attempt_repository_dependency import AttemptRepositoryDependency
from .build_question_repository_dependency import QuestionRepositoryDependency


def build_submit_attempt_use_case(
    enrollment_repository: EnrollmentRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
    question_repository: QuestionRepositoryDependency,
    attempt_repository: AttemptRepositoryDependency,
) -> SubmitAttemptUseCase:
    """Build a SubmitAttemptUseCase with all required injected repositories.

    Args:
        enrollment_repository: Enrollment repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.
        question_repository: Question repository injected by FastAPI.
        attempt_repository: Attempt repository injected by FastAPI.

    Returns:
        SubmitAttemptUseCase: Use case instance ready for execution.
    """
    return SubmitAttemptUseCase(
        enrollment_repository=enrollment_repository,
        module_repository=module_repository,
        question_repository=question_repository,
        attempt_repository=attempt_repository,
    )


SubmitAttemptUseCaseDependency = Annotated[
    SubmitAttemptUseCase,
    Depends(build_submit_attempt_use_case),
]
