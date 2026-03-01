"""Invalid enrollment status transition exception."""

from app.shared.exceptions import UnprocessableException


class InvalidStatusTransitionException(UnprocessableException):
    """Raised when an enrollment status transition is not allowed.

    Args:
        current: The current enrollment status.
        target: The target enrollment status that was rejected.
    """

    def __init__(self, current: str, target: str) -> None:
        """Initialise with the current and target statuses.

        Args:
            current: The current enrollment status value.
            target: The target enrollment status value that was rejected.
        """
        super().__init__(
            message=(f"Cannot transition enrollment from '{current}' to '{target}'."),
            context={"current_status": current, "target_status": target},
            error_code="INVALID_STATUS_TRANSITION",
        )
