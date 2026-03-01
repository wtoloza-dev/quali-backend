"""Build create company use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CreateCompanyUseCase
from .build_company_repository_dependency import CompanyRepositoryDependency


def build_create_company_use_case(
    repository: CompanyRepositoryDependency,
) -> CreateCompanyUseCase:
    """Build a CreateCompanyUseCase with all dependencies injected.

    Intended to be used as a FastAPI Depends() provider. The repository
    is injected automatically via CompanyRepositoryDependency, which
    in turn receives its session from the PostgreSQL session dependency.

    Args:
        repository: Company repository injected by FastAPI.

    Returns:
        CreateCompanyUseCase: Use case instance ready for execution.
    """
    return CreateCompanyUseCase(repository=repository)


CreateCompanyUseCaseDependency = Annotated[
    CreateCompanyUseCase,
    Depends(build_create_company_use_case),
]
