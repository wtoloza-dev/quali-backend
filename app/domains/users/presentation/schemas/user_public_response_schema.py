"""User public response schema."""

from datetime import datetime

from pydantic import BaseModel


class UserPublicResponseSchema(BaseModel):
    """Minimal user data safe to expose publicly.

    Excludes PII fields such as email. Safe to return in contexts where
    full user details are not required.

    Attributes:
        id: ULID of the user.
        first_name: The user's given name.
        last_name: The user's family name.
        created_at: Timestamp when the user profile was created.
    """

    id: str
    first_name: str
    last_name: str
    created_at: datetime
