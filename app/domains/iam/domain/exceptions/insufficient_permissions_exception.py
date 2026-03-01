"""Insufficient permissions exception — re-exports from shared for backwards compatibility.

All new code should import from app.shared.exceptions directly.
"""

from app.shared.exceptions import InsufficientPermissionsException


__all__ = ["InsufficientPermissionsException"]
