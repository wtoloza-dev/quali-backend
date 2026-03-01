"""Build create user use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CreateUserUseCase
from .build_user_repository_dependency import UserRepositoryDependency


def build_create_user_use_case(
    repository: UserRepositoryDependency,
) -> CreateUserUseCase:
    """Build a CreateUserUseCase with all dependencies injected.

    Intended to be used as a FastAPI Depends() provider. The repository
    is injected automatically via UserRepositoryDependency, which
    in turn receives its session from the PostgreSQL session dependency.

    Args:
        repository: User repository injected by FastAPI.

    Returns:
        CreateUserUseCase: Use case instance ready for execution.
    """
    return CreateUserUseCase(repository=repository)


CreateUserUseCaseDependency = Annotated[
    CreateUserUseCase,
    Depends(build_create_user_use_case),
]
