"""Build update company use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateCompanyUseCase
from .build_company_repository_dependency import CompanyRepositoryDependency


def build_update_company_use_case(
    repository: CompanyRepositoryDependency,
) -> UpdateCompanyUseCase:
    """Build an UpdateCompanyUseCase with all dependencies injected.

    Args:
        repository: Company repository injected by FastAPI.

    Returns:
        UpdateCompanyUseCase: Use case instance ready for execution.
    """
    return UpdateCompanyUseCase(repository=repository)


UpdateCompanyUseCaseDependency = Annotated[
    UpdateCompanyUseCase,
    Depends(build_update_company_use_case),
]
