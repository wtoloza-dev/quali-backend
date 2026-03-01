"""User email taken exception."""

from app.shared.exceptions import ConflictException


class UserEmailTakenException(ConflictException):
    """Raised when a user with the given email already exists.

    Args:
        email: The email address that caused the conflict.
    """

    def __init__(self, email: str) -> None:
        """Initialise the exception with the conflicting email.

        Args:
            email: The email address that is already taken.
        """
        super().__init__(
            message=f"A user with email '{email}' already exists.",
            context={"email": email},
            error_code="USER_EMAIL_TAKEN",
        )
