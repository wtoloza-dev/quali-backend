"""Course status enum."""

from enum import StrEnum


class CourseStatus(StrEnum):
    """Lifecycle status of a course.

    Attributes:
        DRAFT: Course is being authored; not visible to learners.
        PUBLISHED: Course is live and available for enrollment.
        ARCHIVED: Course is no longer offered; hidden from new enrollments.
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
