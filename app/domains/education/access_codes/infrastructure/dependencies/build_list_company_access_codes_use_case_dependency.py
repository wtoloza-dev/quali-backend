"""List company access codes use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListCompanyAccessCodesUseCase
from .build_access_code_repository_dependency import AccessCodeRepositoryDependency


def build_list_company_access_codes_use_case(
    repository: AccessCodeRepositoryDependency,
) -> ListCompanyAccessCodesUseCase:
    """Build a ListCompanyAccessCodesUseCase with an injected repository.

    Args:
        repository: Access code repository injected by FastAPI.

    Returns:
        ListCompanyAccessCodesUseCase: Use case instance ready for execution.
    """
    return ListCompanyAccessCodesUseCase(repository=repository)


ListCompanyAccessCodesUseCaseDependency = Annotated[
    ListCompanyAccessCodesUseCase,
    Depends(build_list_company_access_codes_use_case),
]
