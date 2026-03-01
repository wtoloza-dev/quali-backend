"""User not found exception."""

from app.shared.exceptions import NotFoundException


class UserNotFoundException(NotFoundException):
    """Raised when a user lookup by ID returns no result.

    Args:
        user_id: The ULID that was not found.
    """

    def __init__(self, user_id: str) -> None:
        """Initialise the exception with the missing user ID.

        Args:
            user_id: The ULID of the user that was not found.
        """
        super().__init__(
            message=f"User '{user_id}' not found.",
            context={"user_id": user_id},
            error_code="USER_NOT_FOUND",
        )
