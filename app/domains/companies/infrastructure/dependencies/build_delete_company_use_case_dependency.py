"""Build delete company use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import DeleteCompanyUseCase
from .build_company_repository_dependency import CompanyRepositoryDependency


def build_delete_company_use_case(
    repository: CompanyRepositoryDependency,
) -> DeleteCompanyUseCase:
    """Build a DeleteCompanyUseCase with all dependencies injected.

    Args:
        repository: Company repository injected by FastAPI.

    Returns:
        DeleteCompanyUseCase: Use case instance ready for execution.
    """
    return DeleteCompanyUseCase(repository=repository)


DeleteCompanyUseCaseDependency = Annotated[
    DeleteCompanyUseCase,
    Depends(build_delete_company_use_case),
]
