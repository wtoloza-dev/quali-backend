"""Build update user use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import UpdateUserUseCase
from .build_user_repository_dependency import UserRepositoryDependency


def build_update_user_use_case(
    repository: UserRepositoryDependency,
) -> UpdateUserUseCase:
    """Build an UpdateUserUseCase with all dependencies injected.

    Args:
        repository: User repository injected by FastAPI.

    Returns:
        UpdateUserUseCase: Use case instance ready for execution.
    """
    return UpdateUserUseCase(repository=repository)


UpdateUserUseCaseDependency = Annotated[
    UpdateUserUseCase,
    Depends(build_update_user_use_case),
]
