"""Build remove company member use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import RemoveCompanyMemberUseCase
from .build_company_member_repository_dependency import (
    CompanyMemberRepositoryDependency,
)


def build_remove_company_member_use_case(
    repository: CompanyMemberRepositoryDependency,
) -> RemoveCompanyMemberUseCase:
    """Build a RemoveCompanyMemberUseCase with all dependencies injected.

    Args:
        repository: Company member repository injected by FastAPI.

    Returns:
        RemoveCompanyMemberUseCase: Use case instance ready for execution.
    """
    return RemoveCompanyMemberUseCase(repository=repository)


RemoveCompanyMemberUseCaseDependency = Annotated[
    RemoveCompanyMemberUseCase,
    Depends(build_remove_company_member_use_case),
]
