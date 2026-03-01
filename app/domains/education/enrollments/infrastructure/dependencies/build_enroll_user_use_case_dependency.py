"""Enroll user use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import EnrollUserUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_enroll_user_use_case(
    repository: EnrollmentRepositoryDependency,
) -> EnrollUserUseCase:
    """Build an EnrollUserUseCase with an injected repository.

    Args:
        repository: Enrollment repository injected by FastAPI.

    Returns:
        EnrollUserUseCase: Use case instance ready for execution.
    """
    return EnrollUserUseCase(repository=repository)


EnrollUserUseCaseDependency = Annotated[
    EnrollUserUseCase,
    Depends(build_enroll_user_use_case),
]
