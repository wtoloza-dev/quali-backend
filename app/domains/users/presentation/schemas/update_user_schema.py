"""Update user request schema."""

from pydantic import BaseModel


class UpdateUserRequestSchema(BaseModel):
    """Request body for PATCH /api/v1/users/{user_id}.

    Email is excluded because it is immutable after creation.
    All fields are optional to support partial updates.

    Attributes:
        first_name: The user's given name. Optional.
        last_name: The user's family name. Optional.
    """

    first_name: str | None = None
    last_name: str | None = None
    document_type: str | None = None
    document_number: str | None = None
