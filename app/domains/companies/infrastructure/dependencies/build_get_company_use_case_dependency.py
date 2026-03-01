"""Build get company use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetCompanyUseCase
from .build_company_repository_dependency import CompanyRepositoryDependency


def build_get_company_use_case(
    repository: CompanyRepositoryDependency,
) -> GetCompanyUseCase:
    """Build a GetCompanyUseCase with all dependencies injected.

    Args:
        repository: Company repository injected by FastAPI.

    Returns:
        GetCompanyUseCase: Use case instance ready for execution.
    """
    return GetCompanyUseCase(repository=repository)


GetCompanyUseCaseDependency = Annotated[
    GetCompanyUseCase,
    Depends(build_get_company_use_case),
]
