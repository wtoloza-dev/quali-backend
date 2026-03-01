"""Update user use case."""

from ...domain.entities import UserEntity
from ...domain.ports import UserRepositoryPort


class UpdateUserUseCase:
    """Persists a fully merged user entity.

    The caller (presentation layer) is responsible for fetching the existing
    entity, applying the patch, and passing the result here. Email is immutable
    and is never included in updates.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: UserRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(self, entity: UserEntity) -> UserEntity:
        """Persist the updated entity.

        Args:
            entity: Fully merged user entity ready to be persisted.

        Returns:
            UserEntity: The updated entity after persistence.
        """
        return await self._repository.update(entity)
