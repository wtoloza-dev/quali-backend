"""Course access type enum."""

from enum import StrEnum


class AccessType(StrEnum):
    """How a user gained access to a course.

    Attributes:
        COMPANY_ENROLLMENT: HR/manager enrolled the user on behalf of the company.
        PURCHASE: User paid for this specific course (à la carte).
        SUBSCRIPTION: User has an active platform subscription covering all courses.
    """

    COMPANY_ENROLLMENT = "company_enrollment"
    PURCHASE = "purchase"
    SUBSCRIPTION = "subscription"
