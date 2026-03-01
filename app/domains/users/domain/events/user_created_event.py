"""User created domain event."""

from pydantic import BaseModel


class UserCreatedEvent(BaseModel):
    """Emitted when a new user profile is successfully created.

    Consumed by domains that react to user creation, such as
    sending welcome notifications or provisioning default settings.

    Attributes:
        user_id: ID of the newly created user.
        created_by: ID of the actor who triggered the creation.
    """

    user_id: str
    created_by: str
