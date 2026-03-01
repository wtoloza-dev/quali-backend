"""Role enum — re-exports from shared/auth/role.py for backwards compatibility.

All new code should import from app.shared.auth.role directly.
"""

from app.shared.auth.role import ROLE_HIERARCHY, Role


__all__ = ["Role", "ROLE_HIERARCHY"]
