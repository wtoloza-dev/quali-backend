"""Request-scoped authentication context variable."""

from contextvars import ContextVar, Token

from app.shared.exceptions import UnauthorizedException

from .auth_context import AuthContext


_auth_context_var: ContextVar[AuthContext | None] = ContextVar(
    "auth_context", default=None
)


def set_auth_context(ctx: AuthContext) -> Token:
    """Store the authenticated context for the current request.

    Called by AuthMiddleware after a successful JWT decode.

    Args:
        ctx: The authenticated user context to store.

    Returns:
        Token: Reset token that can be passed to reset_auth_context.
    """
    return _auth_context_var.set(ctx)


def reset_auth_context(token: Token) -> None:
    """Reset the auth context to its state before set_auth_context was called.

    Called by AuthMiddleware in a finally block to prevent context
    leaking across requests on the same async task.

    Args:
        token: The reset token returned by set_auth_context.
    """
    _auth_context_var.reset(token)


def get_auth_context() -> AuthContext:
    """Retrieve the authenticated context for the current request.

    This is an internal primitive used by the IAM dependency layer.
    Route handlers should consume auth via ``CurrentUserDependency`` or
    ``require_role()`` instead of calling this function directly — those
    wrappers make auth overridable in tests via ``dependency_overrides``.

    Raises:
        UnauthorizedException: If no auth context has been set (unauthenticated request).

    Returns:
        AuthContext: The authenticated user context.
    """
    ctx = _auth_context_var.get()
    if ctx is None:
        raise UnauthorizedException(
            message="Authentication required.",
            error_code="UNAUTHENTICATED",
        )
    return ctx
