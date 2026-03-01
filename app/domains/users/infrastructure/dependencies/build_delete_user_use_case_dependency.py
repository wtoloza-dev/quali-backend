"""Build delete user use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import DeleteUserUseCase
from .build_user_repository_dependency import UserRepositoryDependency


def build_delete_user_use_case(
    repository: UserRepositoryDependency,
) -> DeleteUserUseCase:
    """Build a DeleteUserUseCase with all dependencies injected.

    Args:
        repository: User repository injected by FastAPI.

    Returns:
        DeleteUserUseCase: Use case instance ready for execution.
    """
    return DeleteUserUseCase(repository=repository)


DeleteUserUseCaseDependency = Annotated[
    DeleteUserUseCase,
    Depends(build_delete_user_use_case),
]
