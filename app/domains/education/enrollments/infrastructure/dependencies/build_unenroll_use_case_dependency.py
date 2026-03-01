"""Unenroll use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UnenrollUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_unenroll_use_case(
    repository: EnrollmentRepositoryDependency,
) -> UnenrollUseCase:
    """Build an UnenrollUseCase with an injected repository.

    Args:
        repository: Enrollment repository injected by FastAPI.

    Returns:
        UnenrollUseCase: Use case instance ready for execution.
    """
    return UnenrollUseCase(repository=repository)


UnenrollUseCaseDependency = Annotated[
    UnenrollUseCase,
    Depends(build_unenroll_use_case),
]
