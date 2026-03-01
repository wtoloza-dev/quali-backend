"""Unauthorized exception."""

from typing import Any

from ._domain_exception import DomainException


class UnauthorizedException(DomainException):
    """Raised when the request lacks valid authentication credentials.

    Example:
        >>> raise UnauthorizedException(
        ...     message="Invalid or expired token.",
        ...     error_code="INVALID_TOKEN",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "UNAUTHORIZED",
    ) -> None:
        """Initialise the unauthorized exception.

        Args:
            message: Human-readable description of the error.
            context: Optional dict with additional structured error context.
            error_code: Machine-readable error code. Defaults to 'UNAUTHORIZED'.
        """
        super().__init__(message=message, context=context, error_code=error_code)
