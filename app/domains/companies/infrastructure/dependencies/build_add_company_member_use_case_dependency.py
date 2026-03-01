"""Build add company member use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import AddCompanyMemberUseCase
from .build_company_member_repository_dependency import (
    CompanyMemberRepositoryDependency,
)


def build_add_company_member_use_case(
    repository: CompanyMemberRepositoryDependency,
) -> AddCompanyMemberUseCase:
    """Build an AddCompanyMemberUseCase with all dependencies injected.

    Args:
        repository: Company member repository injected by FastAPI.

    Returns:
        AddCompanyMemberUseCase: Use case instance ready for execution.
    """
    return AddCompanyMemberUseCase(repository=repository)


AddCompanyMemberUseCaseDependency = Annotated[
    AddCompanyMemberUseCase,
    Depends(build_add_company_member_use_case),
]
