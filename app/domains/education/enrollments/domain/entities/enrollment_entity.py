"""Enrollment domain entity."""

from datetime import datetime

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import EnrollmentStatus


class EnrollmentData(BaseModel):
    """Input fields required to create an enrollment.

    Attributes:
        user_id: ULID of the user being enrolled.
        course_id: ULID of the course to enroll in.
        company_id: ULID of the company context for tenant scoping.
        is_mandatory: Whether completion is required for compliance.
    """

    user_id: str
    course_id: str
    company_id: str
    is_mandatory: bool = False


class EnrollmentEntity(EnrollmentData, AuditEntity):
    """Full persisted enrollment record.

    Attributes:
        status: Current lifecycle state of the enrollment.
        enrolled_at: Timestamp when the enrollment was created.
        completed_at: Timestamp when the enrollment was completed or failed.
    """

    status: EnrollmentStatus = EnrollmentStatus.NOT_STARTED
    enrolled_at: datetime
    completed_at: datetime | None = None
