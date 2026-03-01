"""Create user request schema."""

from pydantic import BaseModel


class CreateUserRequestSchema(BaseModel):
    """Request body for POST /api/v1/users/me.

    Attributes:
        first_name: The user's given name.
        last_name: The user's family name.
    """

    first_name: str = ""
    last_name: str = ""
