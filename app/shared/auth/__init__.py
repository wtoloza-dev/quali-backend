"""Shared authentication context, dependencies, and role enum.

Note: ``require_role`` is intentionally NOT re-exported here to avoid a
circular import chain (auth → contracts → repositories → models → auth).
Import it directly::

    from app.shared.auth.require_role import require_role
"""

from .auth_context import AuthContext
from .auth_context_var import get_auth_context, set_auth_context
from .dependencies import (
    CurrentUserDependency,
    OptionalCurrentUserDependency,
    get_current_user,
    get_optional_current_user,
)
from .role import ROLE_HIERARCHY, Role


__all__ = [
    "AuthContext",
    "get_auth_context",
    "set_auth_context",
    "get_current_user",
    "CurrentUserDependency",
    "get_optional_current_user",
    "OptionalCurrentUserDependency",
    "Role",
    "ROLE_HIERARCHY",
]
