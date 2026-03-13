"""Enrollment status enum."""

from __future__ import annotations

from enum import StrEnum


# Valid transitions: current status → set of allowed next statuses.
_TRANSITIONS: dict[str, set[str]] = {
    "not_started": {"in_progress"},
    "in_progress": {"completed", "failed", "not_started"},
    "completed": {"not_started"},
    "failed": {"not_started"},
}


class EnrollmentStatus(StrEnum):
    """Lifecycle state of a course enrollment.

    Valid transitions:
        not_started → in_progress
        in_progress → completed | failed | not_started  (admin reset)
        completed   → not_started  (admin reset)
        failed      → not_started  (allows reset for re-enrollment)
    """

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

    def can_transition_to(self, target: EnrollmentStatus) -> bool:
        """Return True if transitioning to *target* is allowed.

        Args:
            target: The desired next status.

        Returns:
            bool: True when the transition is valid.
        """
        return target.value in _TRANSITIONS.get(self.value, set())

    def transition_to(self, target: EnrollmentStatus) -> EnrollmentStatus:
        """Return *target* if the transition is valid, otherwise raise.

        Args:
            target: The desired next status.

        Returns:
            EnrollmentStatus: The new status (same object as *target*).

        Raises:
            InvalidStatusTransitionException: If the transition is not allowed.
        """
        if not self.can_transition_to(target):
            from app.domains.education.enrollments.domain.exceptions import (
                InvalidStatusTransitionException,
            )

            raise InvalidStatusTransitionException(
                current=self.value,
                target=target.value,
            )
        return target
