"""Course visibility enum."""

from enum import StrEnum


class CourseVisibility(StrEnum):
    """Who can see and enroll in a course.

    Attributes:
        PUBLIC: Visible to all companies (used by Quali for catalog courses).
        PRIVATE: Visible only to the owning company.
    """

    PUBLIC = "public"
    PRIVATE = "private"
