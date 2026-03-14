"""Search user by email use case."""

from ...domain.entities import UserEntity
from ...domain.ports import UserRepositoryPort


class SearchUserByEmailUseCase:
    """Searches for an active user by exact email match.

    Returns None if no user is found — the caller decides how to handle
    that scenario (e.g. return null to the client, raise an exception).

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: UserRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, email: str) -> UserEntity | None:
        """Execute the search-by-email workflow.

        Args:
            email: Exact email address to search for.

        Returns:
            UserEntity if found, None otherwise.
        """
        return await self._repository.get_by_email(email)
