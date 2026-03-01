"""Delete user use case."""

from ...domain.exceptions import UserNotFoundException
from ...domain.ports import UserRepositoryPort


class DeleteUserUseCase:
    """Hard-deletes a user and archives a tombstone snapshot for audit purposes.

    Validates that the user exists before performing the deletion.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: UserRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, user_id: str, deleted_by: str) -> None:
        """Execute the delete user workflow.

        Args:
            user_id: ULID of the user to delete.
            deleted_by: ID of the actor performing the deletion.

        Raises:
            UserNotFoundException: If no active user exists with the given ID.
        """
        entity = await self._repository.get_by_id(user_id)
        if entity is None:
            raise UserNotFoundException(user_id=user_id)

        await self._repository.delete(
            user_id=user_id,
            deleted_by=deleted_by,
        )
