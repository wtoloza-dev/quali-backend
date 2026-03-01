"""User repository port."""

from typing import Protocol

from ..entities import UserEntity


class UserRepositoryPort(Protocol):
    """Interface for the user repository.

    Defined in the domain layer so the application layer depends on this
    abstraction, not on the concrete SQLModel implementation. The infrastructure
    layer provides the real implementation.
    """

    async def save(self, entity: UserEntity) -> UserEntity:
        """Persist a user entity and return the saved state.

        Args:
            entity: The user entity to persist.

        Returns:
            UserEntity: The persisted entity with any DB-generated fields.
        """
        ...

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Retrieve an active user by its ULID identifier.

        Args:
            user_id: The ULID of the user.

        Returns:
            UserEntity if found, None otherwise.
        """
        ...

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Retrieve an active user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            UserEntity if found, None otherwise.
        """
        ...

    async def update(self, entity: UserEntity) -> UserEntity:
        """Persist changes to an existing user entity.

        Args:
            entity: The user entity with updated fields.

        Returns:
            UserEntity: The updated entity reflecting the persisted state.
        """
        ...

    async def delete(self, user_id: str, deleted_by: str) -> None:
        """Hard-delete a user and archive a tombstone snapshot for audit purposes.

        Args:
            user_id: The ULID of the user to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        ...

    async def list(self, page: int, page_size: int) -> tuple[list[UserEntity], int]:
        """Retrieve a paginated slice of users and the total count.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of UserEntity, total count).
        """
        ...
