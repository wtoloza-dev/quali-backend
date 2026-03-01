"""Build list companies use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListCompaniesUseCase
from .build_company_repository_dependency import CompanyRepositoryDependency


def build_list_companies_use_case(
    repository: CompanyRepositoryDependency,
) -> ListCompaniesUseCase:
    """Build a ListCompaniesUseCase with all dependencies injected.

    Args:
        repository: Company repository injected by FastAPI.

    Returns:
        ListCompaniesUseCase: Use case instance ready for execution.
    """
    return ListCompaniesUseCase(repository=repository)


ListCompaniesUseCaseDependency = Annotated[
    ListCompaniesUseCase,
    Depends(build_list_companies_use_case),
]
