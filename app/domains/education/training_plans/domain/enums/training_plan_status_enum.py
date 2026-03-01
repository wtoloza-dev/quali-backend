"""Training plan status enum."""

from enum import StrEnum


class TrainingPlanStatus(StrEnum):
    """Lifecycle state of an annual training plan.

    Attributes:
        DRAFT: Plan is being defined, not yet active.
        ACTIVE: Plan is in execution for the current year.
        CLOSED: Plan period has ended.
    """

    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
