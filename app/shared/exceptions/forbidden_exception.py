"""Forbidden exception."""

from typing import Any

from ._domain_exception import DomainException


class ForbiddenException(DomainException):
    """Raised when the authenticated user lacks permission for the action.

    Example:
        >>> raise ForbiddenException(
        ...     message="You do not have access to this resource.",
        ...     context={"required_role": "admin"},
        ...     error_code="INSUFFICIENT_PERMISSIONS",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "FORBIDDEN",
    ) -> None:
        """Initialise the forbidden exception.

        Args:
            message: Human-readable description of the error.
            context: Optional dict with additional structured error context.
            error_code: Machine-readable error code. Defaults to 'FORBIDDEN'.
        """
        super().__init__(message=message, context=context, error_code=error_code)
