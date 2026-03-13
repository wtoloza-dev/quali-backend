"""Build update company member use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateCompanyMemberUseCase
from .build_company_member_repository_dependency import (
    CompanyMemberRepositoryDependency,
)


def build_update_company_member_use_case(
    repository: CompanyMemberRepositoryDependency,
) -> UpdateCompanyMemberUseCase:
    """Build an UpdateCompanyMemberUseCase with all dependencies injected.

    Args:
        repository: Company member repository injected by FastAPI.

    Returns:
        UpdateCompanyMemberUseCase: Use case instance ready for execution.
    """
    return UpdateCompanyMemberUseCase(repository=repository)


UpdateCompanyMemberUseCaseDependency = Annotated[
    UpdateCompanyMemberUseCase,
    Depends(build_update_company_member_use_case),
]
