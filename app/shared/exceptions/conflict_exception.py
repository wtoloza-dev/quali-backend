"""Conflict exception."""

from typing import Any

from ._domain_exception import DomainException


class ConflictException(DomainException):
    """Raised when an operation conflicts with the current resource state.

    Domain-specific conflict exceptions should inherit from this class
    and override the default error_code.

    Example:
        >>> raise ConflictException(
        ...     message="A certificate for this user already exists.",
        ...     context={"user_id": "abc"},
        ...     error_code="CERTIFICATE_ALREADY_EXISTS",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "CONFLICT",
    ) -> None:
        """Initialise the conflict exception.

        Args:
            message: Human-readable description of the error.
            context: Optional dict with additional structured error context.
            error_code: Machine-readable error code. Defaults to 'CONFLICT'.
        """
        super().__init__(message=message, context=context, error_code=error_code)
