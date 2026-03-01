"""User access denied exception."""

from app.shared.exceptions import ForbiddenException


class UserAccessDeniedException(ForbiddenException):
    """Raised when an authenticated user tries to access another user's resource.

    Args:
        user_id: The target user ID the caller tried to access.
    """

    def __init__(self, user_id: str) -> None:
        """Initialise the exception with the target user context.

        Args:
            user_id: The target user ID the caller tried to access.
        """
        super().__init__(
            message=f"You do not have permission to access user '{user_id}'.",
            context={"user_id": user_id},
            error_code="USER_ACCESS_DENIED",
        )
