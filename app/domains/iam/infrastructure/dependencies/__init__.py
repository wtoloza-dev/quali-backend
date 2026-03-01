"""Dependency factories for the IAM domain."""

from .current_user_dependency import CurrentUserDependency, get_current_user
from .optional_current_user_dependency import (
    OptionalCurrentUserDependency,
    get_optional_current_user,
)
from .require_role_dependency import require_role


__all__ = [
    "get_current_user",
    "CurrentUserDependency",
    "get_optional_current_user",
    "OptionalCurrentUserDependency",
    "require_role",
]
