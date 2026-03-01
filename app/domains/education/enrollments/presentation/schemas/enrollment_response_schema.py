"""Enrollment response schema."""

from datetime import datetime

from pydantic import BaseModel

from ...domain.enums import EnrollmentStatus


class EnrollmentResponseSchema(BaseModel):
    """Full enrollment response for authenticated users.

    Attributes:
        id: ULID of the enrollment.
        user_id: ULID of the enrolled user.
        course_id: ULID of the course.
        company_id: ULID of the company.
        is_mandatory: Whether completion is required for compliance.
        status: Current enrollment lifecycle state.
        enrolled_at: Timestamp when the enrollment was created.
        completed_at: Timestamp when the enrollment was completed or failed.
        created_at: Audit timestamp.
        created_by: ULID of the creator.
        updated_at: Audit timestamp.
        updated_by: ULID of the last updater.
    """

    id: str
    user_id: str
    course_id: str
    company_id: str
    is_mandatory: bool
    status: EnrollmentStatus
    enrolled_at: datetime
    completed_at: datetime | None
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
