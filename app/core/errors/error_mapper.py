"""Domain exception mapper.

Maps domain exception types to HTTP status codes and builds the
error response body. HTTP concerns stay out of the domain layer.
"""

from fastapi import status

from app.shared.exceptions import (
    ConflictException,
    DomainException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    UnprocessableException,
)


class DomainExceptionMapper:
    """Maps domain exception types to HTTP status codes and response bodies.

    Add domain-specific exceptions here as new bounded contexts are introduced.
    """

    EXCEPTION_STATUS_MAP: dict[type[DomainException], int] = {
        # Shared base exceptions
        NotFoundException: status.HTTP_404_NOT_FOUND,
        ConflictException: status.HTTP_409_CONFLICT,
        UnauthorizedException: status.HTTP_401_UNAUTHORIZED,
        ForbiddenException: status.HTTP_403_FORBIDDEN,
        UnprocessableException: status.HTTP_422_UNPROCESSABLE_CONTENT,
    }

    @classmethod
    def get_status_code(cls, exception: DomainException) -> int:
        """Resolve the HTTP status code for a given domain exception.

        Walks the MRO so subclasses inherit their parent's status code
        without needing to be registered explicitly (Liskov substitution).

        Args:
            exception: The raised domain exception.

        Returns:
            Matching HTTP status code, or 500 if no registered type is found.
        """
        for exc_type in type(exception).__mro__:
            if exc_type in cls.EXCEPTION_STATUS_MAP:
                return cls.EXCEPTION_STATUS_MAP[exc_type]
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    @classmethod
    def get_response_body(cls, exception: DomainException) -> dict:
        """Build the JSON response body for a domain exception.

        Args:
            exception: The raised domain exception.

        Returns:
            Dict with error_code, message, and context fields.
        """
        return {
            "error_code": exception.error_code,
            "message": exception.message,
            "context": exception.context,
        }
