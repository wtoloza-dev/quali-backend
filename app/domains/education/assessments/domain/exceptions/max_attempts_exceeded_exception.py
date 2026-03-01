"""Max attempts exceeded exception."""

from app.shared.exceptions import ConflictException


class MaxAttemptsExceededException(ConflictException):
    """Raised when a student has exhausted all allowed assessment attempts.

    Args:
        enrollment_id: ULID of the enrollment that has no remaining attempts.
        max_attempts: The maximum number of attempts configured for the course.
    """

    def __init__(self, enrollment_id: str, max_attempts: int) -> None:
        """Initialise with the enrollment and max attempts count.

        Args:
            enrollment_id: ULID of the enrollment.
            max_attempts: The course-configured maximum.
        """
        super().__init__(
            message=(
                f"Maximum attempts ({max_attempts}) reached "
                f"for enrollment '{enrollment_id}'."
            ),
            context={"enrollment_id": enrollment_id, "max_attempts": max_attempts},
            error_code="MAX_ATTEMPTS_EXCEEDED",
        )
