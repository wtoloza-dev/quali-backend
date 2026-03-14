"""Admin list attempts use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import AdminListAttemptsUseCase
from .build_attempt_repository_dependency import AttemptRepositoryDependency


def build_admin_list_attempts_use_case(
    repository: AttemptRepositoryDependency,
) -> AdminListAttemptsUseCase:
    """Build an AdminListAttemptsUseCase with injected repositories.

    Args:
        repository: Attempt repository injected by FastAPI.

    Returns:
        AdminListAttemptsUseCase: Use case instance ready for execution.
    """
    return AdminListAttemptsUseCase(repository=repository)


AdminListAttemptsUseCaseDependency = Annotated[
    AdminListAttemptsUseCase,
    Depends(build_admin_list_attempts_use_case),
]
