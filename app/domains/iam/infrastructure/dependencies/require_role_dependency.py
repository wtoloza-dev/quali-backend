"""Require role dependency — re-exports from shared for backwards compatibility.

All new code should import from app.shared.auth.require_role directly.
"""

from app.shared.auth.require_role import require_role


__all__ = ["require_role"]
