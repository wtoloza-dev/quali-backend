"""Superadmin impersonation dependency.

Allows superadmins to act as another user by sending the
``X-Impersonate-User`` header alongside their own Bearer JWT.
The dependency verifies that the caller is a superadmin, then swaps
the AuthContext so downstream code sees the impersonated user.

The real superadmin's ULID is preserved in ``AuthContext.real_user_id``
for audit purposes.

Import this dependency directly — it is intentionally NOT re-exported
from ``app.shared.auth.__init__`` to avoid the same circular-import
chain as ``require_role``.
"""

import logging
from typing import Annotated

from fastapi import Depends, Header

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.contracts.get_user_by_id.get_user_by_id_adapter import (
    GetUserByIdDependency,
)
from app.shared.exceptions import ForbiddenException

logger = logging.getLogger(__name__)

_IMPERSONATE_HEADER = "x-impersonate-user"


async def get_impersonated_user(
    auth: CurrentUserDependency,
    get_user: GetUserByIdDependency,
    x_impersonate_user: Annotated[str | None, Header()] = None,
) -> AuthContext:
    """Resolve the effective AuthContext, applying impersonation if requested.

    When the ``X-Impersonate-User`` header is absent, returns the
    original AuthContext unchanged.  When present, verifies that the
    caller is a superadmin and returns a new AuthContext with the
    impersonated user's ULID.

    Args:
        auth: The authenticated superadmin context from the JWT.
        get_user: Contract adapter to look up user details.
        x_impersonate_user: Target user ULID from the request header.

    Returns:
        AuthContext: The effective context (original or impersonated).

    Raises:
        ForbiddenException: If the caller is not a superadmin or the
            target user does not exist.
    """
    if x_impersonate_user is None:
        return auth

    # Verify the caller is a superadmin.
    caller = await get_user(user_id=auth.user_id)
    if not caller or not caller.is_superadmin:
        raise ForbiddenException(
            message="Only superadmins can impersonate users.",
            context={"user_id": auth.user_id},
            error_code="IMPERSONATION_FORBIDDEN",
        )

    # Verify the target user exists.
    target = await get_user(user_id=x_impersonate_user)
    if not target:
        raise ForbiddenException(
            message=f"Target user '{x_impersonate_user}' not found.",
            context={"target_user_id": x_impersonate_user},
            error_code="IMPERSONATION_TARGET_NOT_FOUND",
        )

    logger.warning(
        "Impersonation active: superadmin %s acting as user %s (%s)",
        auth.user_id,
        target.id,
        target.email,
    )

    return AuthContext(
        user_id=target.id,
        email=target.email,
        real_user_id=auth.user_id,
    )


ImpersonatedUserDependency = Annotated[
    AuthContext, Depends(get_impersonated_user)
]
