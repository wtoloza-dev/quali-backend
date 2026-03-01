"""Not found exception."""

from typing import Any

from ._domain_exception import DomainException


class NotFoundException(DomainException):
    """Raised when a requested resource does not exist.

    Domain-specific not-found exceptions should inherit from this class
    and override the default error_code.

    Example:
        >>> raise NotFoundException(
        ...     message="Certificate '123' not found.",
        ...     context={"certificate_id": "123"},
        ...     error_code="CERTIFICATE_NOT_FOUND",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "NOT_FOUND",
    ) -> None:
        """Initialise the not found exception.

        Args:
            message: Human-readable description of the error.
            context: Optional dict with additional structured error context.
            error_code: Machine-readable error code. Defaults to 'NOT_FOUND'.
        """
        super().__init__(message=message, context=context, error_code=error_code)
