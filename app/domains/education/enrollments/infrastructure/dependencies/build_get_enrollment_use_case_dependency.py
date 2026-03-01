"""Get enrollment use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetEnrollmentUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_get_enrollment_use_case(
    repository: EnrollmentRepositoryDependency,
) -> GetEnrollmentUseCase:
    """Build a GetEnrollmentUseCase with an injected repository.

    Args:
        repository: Enrollment repository injected by FastAPI.

    Returns:
        GetEnrollmentUseCase: Use case instance ready for execution.
    """
    return GetEnrollmentUseCase(repository=repository)


GetEnrollmentUseCaseDependency = Annotated[
    GetEnrollmentUseCase,
    Depends(build_get_enrollment_use_case),
]
