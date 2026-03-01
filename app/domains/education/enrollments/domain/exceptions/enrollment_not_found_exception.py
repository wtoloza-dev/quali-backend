"""Enrollment not found exception."""

from app.shared.exceptions import NotFoundException


class EnrollmentNotFoundException(NotFoundException):
    """Raised when an enrollment cannot be found by the given ID.

    Args:
        enrollment_id: The ULID that was not found.
    """

    def __init__(self, enrollment_id: str) -> None:
        """Initialise with the missing enrollment ID.

        Args:
            enrollment_id: The ULID that was not found.
        """
        super().__init__(
            message=f"Enrollment '{enrollment_id}' not found.",
            context={"enrollment_id": enrollment_id},
            error_code="ENROLLMENT_NOT_FOUND",
        )
