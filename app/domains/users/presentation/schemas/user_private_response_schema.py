"""User private response schema."""

from datetime import datetime

from pydantic import BaseModel


class UserPrivateResponseSchema(BaseModel):
    """Full user data returned to authenticated callers.

    Includes PII fields such as email and the complete audit trail.

    Attributes:
        id: ULID of the user.
        first_name: The user's given name.
        last_name: The user's family name.
        email: Primary contact email.
        created_at: Timestamp when the user profile was created.
        created_by: ID of the actor who created the profile.
        updated_at: Timestamp of the last update, managed by the DB.
        updated_by: ID of the actor who last updated the profile.
    """

    id: str
    first_name: str
    last_name: str
    email: str
    document_type: str | None
    document_number: str | None
    is_superadmin: bool
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
