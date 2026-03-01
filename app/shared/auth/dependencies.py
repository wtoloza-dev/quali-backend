"""Authentication FastAPI dependencies.

Provides injectable dependencies for route handlers that need the
authenticated user context. These are placed in shared/ because they
are cross-cutting infrastructure used by every domain.
"""

from typing import Annotated

from fastapi import Depends

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.auth_context_var import get_auth_context
from app.shared.exceptions import UnauthorizedException


def get_current_user() -> AuthContext:
    """Return the authenticated user context for the current request.

    The context was populated by AuthMiddleware from the JWT in the
    Authorization header — no token extraction happens here.

    Returns:
        AuthContext: The authenticated user context.

    Raises:
        UnauthorizedException: If AuthMiddleware found no valid token.
    """
    return get_auth_context()


CurrentUserDependency = Annotated[AuthContext, Depends(get_current_user)]


def get_optional_current_user() -> AuthContext | None:
    """Return the authenticated user context, or None if not authenticated.

    Unlike CurrentUserDependency, this never raises. Use it on public routes
    that serve different responses for authenticated vs unauthenticated users.

    Returns:
        AuthContext if a valid JWT was present, None otherwise.
    """
    try:
        return get_auth_context()
    except UnauthorizedException:
        return None


OptionalCurrentUserDependency = Annotated[
    AuthContext | None,
    Depends(get_optional_current_user),
]
