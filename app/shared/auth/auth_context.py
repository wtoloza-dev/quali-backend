"""Authentication context injected into protected route handlers."""

from pydantic import BaseModel


class AuthContext(BaseModel):
    """Represents the authenticated actor for the current request.

    Extracted from the JWT access token by CurrentUserDependency and
    injected into any route that requires authentication.

    When a superadmin impersonates another user, ``user_id`` is set to
    the impersonated user and ``real_user_id`` holds the superadmin's
    ULID for audit purposes.

    Attributes:
        user_id: ULID of the effective user (impersonated or real).
        email: Email address of the authenticated user.
        real_user_id: ULID of the actual superadmin when impersonating.
            None for normal (non-impersonated) requests.
    """

    user_id: str
    email: str
    real_user_id: str | None = None

    @property
    def is_impersonating(self) -> bool:
        """Return True if this request is an impersonated session."""
        return self.real_user_id is not None

    @property
    def audit_user_id(self) -> str:
        """Return the real actor ID for audit fields (created_by, etc.).

        When impersonating, returns the superadmin's ID so that audit
        trails always reflect who actually performed the action.
        """
        return self.real_user_id or self.user_id
