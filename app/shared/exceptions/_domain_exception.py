"""Base domain exception. Not intended to be raised directly — extend it."""

from typing import Any


class DomainException(Exception):
    """Base exception for all domain-level errors.

    Carry a machine-readable error_code, a human-readable message,
    and optional structured context. HTTP mapping is handled outside
    the domain layer. Do not raise this class directly — use a
    specific subclass.

    Attributes:
        error_code: Machine-readable identifier for the exception type.
        message: Human-readable description of the error.
        context: Optional structured data providing additional error context.
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "DOMAIN_ERROR",
    ) -> None:
        """Initialise the domain exception.

        Args:
            message: Human-readable description of the error.
            context: Optional dict with additional structured error context.
            error_code: Machine-readable error code for this exception type.
        """
        self.error_code = error_code
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return a structured string representation of the exception.

        Returns:
            Formatted string including class name, error code, and message.
        """
        return f"{self.__class__.__name__} [{self.error_code}]: {self.message}"
