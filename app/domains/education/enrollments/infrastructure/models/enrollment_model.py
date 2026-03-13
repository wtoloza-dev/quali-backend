"""Enrollment ORM model."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlmodel import Field

from app.shared.models.audit_model import AuditModel

from ...domain.enums import AccessType, EnrollmentStatus


class EnrollmentModel(AuditModel, table=True):
    """SQLModel ORM model for the enrollments table.

    Attributes:
        __tablename__: Database table name.
        user_id: ULID of the enrolled user.
        course_id: ULID of the course.
        is_mandatory: Whether the enrollment is mandatory.
        status: Current enrollment lifecycle state.
        access_type: Content access level (preview or full).
        enrolled_at: Timestamp when the enrollment was created.
        completed_at: Timestamp when the enrollment was completed or failed.
        start_date: When full access begins.
        end_date: When full access expires.
    """

    __tablename__ = "enrollments"
    __table_args__ = (
        sa.UniqueConstraint("user_id", "course_id", name="uq_enrollments_user_course"),
    )

    user_id: str = Field(nullable=False, index=True)
    course_id: str = Field(nullable=False, index=True)
    is_mandatory: bool = Field(default=False, nullable=False)
    status: EnrollmentStatus = Field(
        default=EnrollmentStatus.NOT_STARTED,
        sa_type=sa.String(),
        nullable=False,
    )
    access_type: AccessType = Field(
        default=AccessType.PREVIEW,
        sa_type=sa.String(),
        nullable=False,
    )
    enrolled_at: datetime = Field(
        nullable=False,
        sa_type=DateTime(timezone=True),
    )
    completed_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
    start_date: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
    end_date: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
