"""List attempts use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.enrollments.infrastructure.dependencies import (
    EnrollmentRepositoryDependency,
)

from ...application.use_cases import ListAttemptsUseCase
from .build_attempt_repository_dependency import AttemptRepositoryDependency


def build_list_attempts_use_case(
    repository: AttemptRepositoryDependency,
    enrollment_repository: EnrollmentRepositoryDependency,
) -> ListAttemptsUseCase:
    """Build a ListAttemptsUseCase with injected repositories.

    Args:
        repository: Attempt repository injected by FastAPI.
        enrollment_repository: Enrollment repository for ownership checks.

    Returns:
        ListAttemptsUseCase: Use case instance ready for execution.
    """
    return ListAttemptsUseCase(
        repository=repository,
        enrollment_repository=enrollment_repository,
    )


ListAttemptsUseCaseDependency = Annotated[
    ListAttemptsUseCase,
    Depends(build_list_attempts_use_case),
]
