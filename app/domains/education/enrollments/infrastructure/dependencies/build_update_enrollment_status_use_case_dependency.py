"""Update enrollment status use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateEnrollmentStatusUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_update_enrollment_status_use_case(
    repository: EnrollmentRepositoryDependency,
) -> UpdateEnrollmentStatusUseCase:
    """Build an UpdateEnrollmentStatusUseCase with an injected repository.

    Args:
        repository: Enrollment repository injected by FastAPI.

    Returns:
        UpdateEnrollmentStatusUseCase: Use case instance ready for execution.
    """
    return UpdateEnrollmentStatusUseCase(repository=repository)


UpdateEnrollmentStatusUseCaseDependency = Annotated[
    UpdateEnrollmentStatusUseCase,
    Depends(build_update_enrollment_status_use_case),
]
