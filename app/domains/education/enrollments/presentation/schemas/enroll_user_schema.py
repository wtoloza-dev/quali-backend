"""Enroll user request schema."""

from pydantic import BaseModel


class EnrollUserRequestSchema(BaseModel):
    """Request body for enrolling a user in a course.

    Attributes:
        course_id: ULID of the course.
        is_mandatory: Whether completion is required for compliance.
        legal_accepted: Must be True — confirms the user accepted the legal declaration.
    """

    course_id: str
    is_mandatory: bool = False
    legal_accepted: bool
