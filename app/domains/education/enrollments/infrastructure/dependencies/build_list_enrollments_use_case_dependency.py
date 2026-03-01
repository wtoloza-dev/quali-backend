"""List enrollments use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListEnrollmentsUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_list_enrollments_use_case(
    repository: EnrollmentRepositoryDependency,
) -> ListEnrollmentsUseCase:
    """Build a ListEnrollmentsUseCase with an injected repository.

    Args:
        repository: Enrollment repository injected by FastAPI.

    Returns:
        ListEnrollmentsUseCase: Use case instance ready for execution.
    """
    return ListEnrollmentsUseCase(repository=repository)


ListEnrollmentsUseCaseDependency = Annotated[
    ListEnrollmentsUseCase,
    Depends(build_list_enrollments_use_case),
]
