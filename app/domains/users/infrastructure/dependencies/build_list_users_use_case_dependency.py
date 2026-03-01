"""Build list users use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListUsersUseCase
from .build_user_repository_dependency import UserRepositoryDependency


def build_list_users_use_case(
    repository: UserRepositoryDependency,
) -> ListUsersUseCase:
    """Build a ListUsersUseCase with all dependencies injected.

    Args:
        repository: User repository injected by FastAPI.

    Returns:
        ListUsersUseCase: Use case instance ready for execution.
    """
    return ListUsersUseCase(repository=repository)


ListUsersUseCaseDependency = Annotated[
    ListUsersUseCase,
    Depends(build_list_users_use_case),
]
