"""Authentication context injected into protected route handlers."""

from pydantic import BaseModel


class AuthContext(BaseModel):
    """Represents the authenticated actor for the current request.

    Extracted from the JWT access token by CurrentUserDependency and
    injected into any route that requires authentication.

    Attributes:
        user_id: ULID of the authenticated user.
        email: Email address of the authenticated user.
    """

    user_id: str
    email: str
