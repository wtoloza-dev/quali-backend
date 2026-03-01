"""Optional current user dependency — re-exports from shared for backwards compatibility.

All new code should import from app.shared.auth.dependencies directly.
"""

from app.shared.auth.dependencies import (
    OptionalCurrentUserDependency,
    get_optional_current_user,
)


__all__ = ["OptionalCurrentUserDependency", "get_optional_current_user"]
