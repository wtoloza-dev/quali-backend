"""List attempts use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListAttemptsUseCase
from .build_attempt_repository_dependency import AttemptRepositoryDependency


def build_list_attempts_use_case(
    repository: AttemptRepositoryDependency,
) -> ListAttemptsUseCase:
    """Build a ListAttemptsUseCase with an injected repository.

    Args:
        repository: Attempt repository injected by FastAPI.

    Returns:
        ListAttemptsUseCase: Use case instance ready for execution.
    """
    return ListAttemptsUseCase(repository=repository)


ListAttemptsUseCaseDependency = Annotated[
    ListAttemptsUseCase,
    Depends(build_list_attempts_use_case),
]
