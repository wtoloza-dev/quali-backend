"""Enrollment response schema."""

from datetime import datetime

from pydantic import BaseModel

from ...domain.enums import AccessType, EnrollmentStatus


class EnrollmentResponseSchema(BaseModel):
    """Full enrollment response for authenticated users.

    Attributes:
        id: ULID of the enrollment.
        user_id: ULID of the enrolled user.
        course_id: ULID of the course.
        is_mandatory: Whether completion is required for compliance.
        status: Current enrollment lifecycle state.
        access_type: Content access level (preview or full).
        enrolled_at: Timestamp when the enrollment was created.
        completed_at: Timestamp when the enrollment was completed or failed.
        start_date: When full access begins.
        end_date: When full access expires.
        created_at: Audit timestamp.
        created_by: ULID of the creator.
        updated_at: Audit timestamp.
        updated_by: ULID of the last updater.
    """

    id: str
    user_id: str
    course_id: str
    is_mandatory: bool
    status: EnrollmentStatus
    access_type: AccessType
    enrolled_at: datetime
    completed_at: datetime | None
    start_date: datetime | None
    end_date: datetime | None
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
    user_email: str | None = None
    user_first_name: str | None = None
    user_last_name: str | None = None
