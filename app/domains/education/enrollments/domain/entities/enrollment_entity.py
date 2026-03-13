"""Enrollment domain entity."""

from datetime import datetime

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import AccessType, EnrollmentStatus


class EnrollmentData(BaseModel):
    """Input fields required to create an enrollment.

    Attributes:
        user_id: ULID of the user being enrolled.
        course_id: ULID of the course to enroll in.
        is_mandatory: Whether completion is required for compliance.
    """

    user_id: str
    course_id: str
    is_mandatory: bool = False


class EnrollmentEntity(EnrollmentData, AuditEntity):
    """Full persisted enrollment record.

    Attributes:
        status: Current lifecycle state of the enrollment.
        access_type: Content access level (preview or full).
        enrolled_at: Timestamp when the enrollment was created.
        completed_at: Timestamp when the enrollment was completed or failed.
        start_date: When full access begins.
        end_date: When full access expires (None means permanent).
    """

    status: EnrollmentStatus = EnrollmentStatus.NOT_STARTED
    access_type: AccessType = AccessType.PREVIEW
    enrolled_at: datetime
    completed_at: datetime | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
