"""Get user use case."""

from ...domain.entities import UserEntity
from ...domain.exceptions import UserNotFoundException
from ...domain.ports import UserRepositoryPort


class GetUserUseCase:
    """Retrieves an active user by their ULID.

    Raises NotFoundException if the user does not exist or has been
    permanently deleted.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: UserRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, user_id: str) -> UserEntity:
        """Execute the get user workflow.

        Args:
            user_id: ULID of the user to retrieve.

        Returns:
            UserEntity: The active user entity.

        Raises:
            UserNotFoundException: If no active user exists with the given ID.
        """
        entity = await self._repository.get_by_id(user_id)
        if entity is None:
            raise UserNotFoundException(user_id=user_id)
        return entity
