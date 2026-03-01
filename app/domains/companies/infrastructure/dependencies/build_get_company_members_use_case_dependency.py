"""Build get company members use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetCompanyMembersUseCase
from .build_company_member_repository_dependency import (
    CompanyMemberRepositoryDependency,
)


def build_get_company_members_use_case(
    repository: CompanyMemberRepositoryDependency,
) -> GetCompanyMembersUseCase:
    """Build a GetCompanyMembersUseCase with all dependencies injected.

    Args:
        repository: Company member repository injected by FastAPI.

    Returns:
        GetCompanyMembersUseCase: Use case instance ready for execution.
    """
    return GetCompanyMembersUseCase(repository=repository)


GetCompanyMembersUseCaseDependency = Annotated[
    GetCompanyMembersUseCase,
    Depends(build_get_company_members_use_case),
]
