"""Insufficient permissions exception."""

from app.shared.exceptions.forbidden_exception import ForbiddenException


class InsufficientPermissionsException(ForbiddenException):
    """Raised when the authenticated user lacks the required role.

    Args:
        required_role: The minimum role required for the operation.
        company_id: The company context in which the check failed.
    """

    def __init__(self, required_role: str, company_id: str) -> None:
        """Initialise the exception with role and company context.

        Args:
            required_role: The minimum role required for the operation.
            company_id: The company context in which the check failed.
        """
        super().__init__(
            message=(
                f"Role '{required_role}' or higher is required "
                f"for company '{company_id}'."
            ),
            context={"required_role": required_role, "company_id": company_id},
            error_code="INSUFFICIENT_PERMISSIONS",
        )
