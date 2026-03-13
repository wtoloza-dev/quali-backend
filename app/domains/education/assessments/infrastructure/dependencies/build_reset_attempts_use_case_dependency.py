"""Reset attempts use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.enrollments.infrastructure.dependencies import (
    EnrollmentRepositoryDependency,
)

from ...application.use_cases import ResetAttemptsUseCase
from .build_attempt_repository_dependency import AttemptRepositoryDependency


def build_reset_attempts_use_case(
    attempt_repository: AttemptRepositoryDependency,
    enrollment_repository: EnrollmentRepositoryDependency,
) -> ResetAttemptsUseCase:
    """Build a ResetAttemptsUseCase with injected repositories.

    Args:
        attempt_repository: Attempt repository injected by FastAPI.
        enrollment_repository: Enrollment repository injected by FastAPI.

    Returns:
        ResetAttemptsUseCase: Use case instance ready for execution.
    """
    return ResetAttemptsUseCase(
        attempt_repository=attempt_repository,
        enrollment_repository=enrollment_repository,
    )


ResetAttemptsUseCaseDependency = Annotated[
    ResetAttemptsUseCase,
    Depends(build_reset_attempts_use_case),
]
