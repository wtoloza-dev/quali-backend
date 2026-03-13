"""List company enrollments use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListCompanyEnrollmentsUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_list_company_enrollments_use_case(
    repository: EnrollmentRepositoryDependency,
) -> ListCompanyEnrollmentsUseCase:
    """Build a ListCompanyEnrollmentsUseCase with an injected repository.

    Args:
        repository: Enrollment repository injected by FastAPI.

    Returns:
        ListCompanyEnrollmentsUseCase: Use case instance ready for execution.
    """
    return ListCompanyEnrollmentsUseCase(repository=repository)


ListCompanyEnrollmentsUseCaseDependency = Annotated[
    ListCompanyEnrollmentsUseCase,
    Depends(build_list_company_enrollments_use_case),
]
