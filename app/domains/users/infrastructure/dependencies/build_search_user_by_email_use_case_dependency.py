"""Build search user by email use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import SearchUserByEmailUseCase
from .build_user_repository_dependency import UserRepositoryDependency


def build_search_user_by_email_use_case(
    repository: UserRepositoryDependency,
) -> SearchUserByEmailUseCase:
    """Build a SearchUserByEmailUseCase with all dependencies injected.

    Args:
        repository: User repository injected by FastAPI.

    Returns:
        SearchUserByEmailUseCase: Use case instance ready for execution.
    """
    return SearchUserByEmailUseCase(repository=repository)


SearchUserByEmailUseCaseDependency = Annotated[
    SearchUserByEmailUseCase,
    Depends(build_search_user_by_email_use_case),
]
