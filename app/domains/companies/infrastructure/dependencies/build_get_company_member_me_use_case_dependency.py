"""Build get company member me use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetCompanyMemberMeUseCase
from .build_company_member_repository_dependency import (
    CompanyMemberRepositoryDependency,
)


def build_get_company_member_me_use_case(
    repository: CompanyMemberRepositoryDependency,
) -> GetCompanyMemberMeUseCase:
    """Build a GetCompanyMemberMeUseCase with all dependencies injected.

    Args:
        repository: Company member repository injected by FastAPI.

    Returns:
        GetCompanyMemberMeUseCase: Use case instance ready for execution.
    """
    return GetCompanyMemberMeUseCase(repository=repository)


GetCompanyMemberMeUseCaseDependency = Annotated[
    GetCompanyMemberMeUseCase,
    Depends(build_get_company_member_me_use_case),
]
