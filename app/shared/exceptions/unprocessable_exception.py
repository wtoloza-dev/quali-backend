"""Unprocessable exception."""

from typing import Any

from ._domain_exception import DomainException


class UnprocessableException(DomainException):
    """Raised when input is syntactically valid but semantically incorrect.

    Example:
        >>> raise UnprocessableException(
        ...     message="Expiry date must be after issue date.",
        ...     context={"issued_at": "2025-01-01", "expires_at": "2024-01-01"},
        ...     error_code="INVALID_DATE_RANGE",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "UNPROCESSABLE",
    ) -> None:
        """Initialise the unprocessable exception.

        Args:
            message: Human-readable description of the error.
            context: Optional dict with additional structured error context.
            error_code: Machine-readable error code. Defaults to 'UNPROCESSABLE'.
        """
        super().__init__(message=message, context=context, error_code=error_code)
