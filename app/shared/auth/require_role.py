"""Role guard dependency factory.

Provides a FastAPI dependency that enforces a minimum company role for the
authenticated user. Placed in shared/ because it is used across every domain
that needs company-scoped authorisation.
"""

from typing import Annotated

from fastapi import Depends, Path

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.auth.role import ROLE_HIERARCHY, Role
from app.shared.contracts.get_company_member import GetCompanyMemberDependency
from app.shared.contracts.get_user_by_id import GetUserByIdDependency
from app.shared.exceptions import InsufficientPermissionsException


def require_role(minimum_role: Role, company_id_path_param: str = "company_id"):
    """Build a FastAPI dependency that enforces a minimum role for a company.

    The dependency resolves the company_id from the request path, queries
    the company_members table for the authenticated user, and raises
    InsufficientPermissionsException if the user's role is below the minimum.

    The role hierarchy is respected: OWNER passes an ADMIN guard, ADMIN
    passes a MEMBER guard, and so on.

    Args:
        minimum_role: The lowest role level that is allowed through.
        company_id_path_param: Name of the path parameter that holds the
            company ULID. Defaults to "company_id".

    Returns:
        A FastAPI Depends()-compatible callable that yields AuthContext.

    Example:
        @router.delete("/{company_id}")
        async def delete_company(
            company_id: str,
            auth: Annotated[AuthContext, require_role(Role.OWNER)],
        ) -> ...:
            ...
    """

    async def guard(
        company_id: Annotated[str, Path(alias=company_id_path_param)],
        member_adapter: GetCompanyMemberDependency,
        user_adapter: GetUserByIdDependency,
        auth: CurrentUserDependency,
    ) -> AuthContext:
        """Enforce the minimum role for the current request.

        Superadmins bypass role checks entirely. Regular users must hold
        the minimum role (or higher) in the target company.

        Args:
            company_id: Resolved from the request path.
            member_adapter: Injected company member contract adapter.
            user_adapter: Injected user contract adapter for superadmin check.
            auth: Authenticated user context injected via CurrentUserDependency.

        Returns:
            AuthContext: The authenticated user context if authorised.

        Raises:
            UnauthorizedException: If no JWT was provided.
            InsufficientPermissionsException: If the user's role is too low.
        """
        # Superadmins bypass all company role checks.
        user = await user_adapter(user_id=auth.user_id)
        if user and user.is_superadmin:
            return auth

        member = await member_adapter(company_id=company_id, user_id=auth.user_id)
        if member is None:
            raise InsufficientPermissionsException(
                required_role=minimum_role,
                company_id=company_id,
            )

        user_weight = ROLE_HIERARCHY[Role(member.role)]
        required_weight = ROLE_HIERARCHY[minimum_role]

        if user_weight < required_weight:
            raise InsufficientPermissionsException(
                required_role=minimum_role,
                company_id=company_id,
            )

        return auth

    return Depends(guard)
