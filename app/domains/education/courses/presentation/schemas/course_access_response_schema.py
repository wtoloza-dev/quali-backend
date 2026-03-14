"""Course access check response schema."""

from pydantic import BaseModel


class CourseAccessResponseSchema(BaseModel):
    """Response indicating whether the user has full access to a course.

    Attributes:
        has_access: True if the user has an active access grant.
    """

    has_access: bool
