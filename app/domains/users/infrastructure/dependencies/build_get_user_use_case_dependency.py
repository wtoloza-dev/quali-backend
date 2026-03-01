"""Build get user use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetUserUseCase
from .build_user_repository_dependency import UserRepositoryDependency


def build_get_user_use_case(
    repository: UserRepositoryDependency,
) -> GetUserUseCase:
    """Build a GetUserUseCase with all dependencies injected.

    Args:
        repository: User repository injected by FastAPI.

    Returns:
        GetUserUseCase: Use case instance ready for execution.
    """
    return GetUserUseCase(repository=repository)


GetUserUseCaseDependency = Annotated[
    GetUserUseCase,
    Depends(build_get_user_use_case),
]
