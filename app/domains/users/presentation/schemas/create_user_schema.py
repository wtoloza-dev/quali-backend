"""Create user request schema."""

from pydantic import BaseModel, field_validator


class CreateUserRequestSchema(BaseModel):
    """Request body for POST /api/v1/users/me.

    Attributes:
        first_name: The user's given name.
        last_name: The user's family name.
    """

    first_name: str = ""
    last_name: str = ""

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Normalize name fields to title case."""
        return value.strip().title() if value else value
