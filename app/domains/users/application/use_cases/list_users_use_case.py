"""List users use case."""

from ...domain.entities import UserEntity
from ...domain.ports.user_repository_port import UserRepositoryPort


class ListUsersUseCase:
    """Return a paginated list of active users.

    Delegates entirely to the repository — no business logic is applied
    beyond what the port contract already guarantees (soft-delete filtering).

    Attributes:
        _repository: The user repository port implementation.
    """

    def __init__(self, repository: UserRepositoryPort) -> None:
        """Initialise the use case with its repository dependency.

        Args:
            repository: An implementation of UserRepositoryPort.
        """
        self._repository = repository

    async def execute(self, page: int, page_size: int) -> tuple[list[UserEntity], int]:
        """Retrieve a paginated slice of users and the total count.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of UserEntity, total active user count).
        """
        return await self._repository.list(page=page, page_size=page_size)
