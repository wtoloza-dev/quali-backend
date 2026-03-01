"""Create user use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import UserData, UserEntity
from ...domain.exceptions import UserEmailTakenException
from ...domain.ports import UserRepositoryPort


class CreateUserUseCase:
    """Handles the creation of a new user profile.

    Validates that the email is not already taken by an active user,
    constructs the user entity, and persists it via the repository.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: UserRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self, data: UserData, created_by: str, user_id: str | None = None
    ) -> UserEntity:
        """Execute the user creation workflow.

        Args:
            data: Validated user data from the presentation layer.
            created_by: ULID of the actor creating the user. On self-registration
                this should equal user_id so the audit trail shows the user created
                their own account.
            user_id: Optional pre-generated ULID for the new user. If omitted a new
                ULID is generated internally. Pass an explicit value when the caller
                needs to know the ID before calling this method (e.g. self-registration
                where created_by must equal the new user's own ID).

        Returns:
            UserEntity: The persisted user entity.

        Raises:
            UserEmailTakenException: If an active user with the same email already exists.
        """
        existing = await self._repository.get_by_email(data.email)
        if existing:
            raise UserEmailTakenException(email=data.email)

        now = datetime.now(UTC)
        entity = UserEntity(
            id=user_id if user_id is not None else str(ULID()),
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
