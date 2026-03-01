"""Course access SQLModel ORM model."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlmodel import Field

from app.shared.models import AuditModel

from ...domain.enums import AccessType


class CourseAccessModel(AuditModel, table=True):
    """SQLModel ORM representation of the course_access table.

    Each row represents a user's right to access a course.
    Multiple rows for the same user+course are allowed (e.g. subscription
    renewed after expiry).

    Attributes:
        __tablename__: Database table name.
        user_id: The user who has access (indexed).
        course_id: The course being unlocked (indexed).
        access_type: How access was granted.
        expires_at: When the access expires. None means permanent.
    """

    __tablename__ = "course_access"

    user_id: str = Field(nullable=False, index=True)
    course_id: str = Field(nullable=False, index=True)
    access_type: AccessType = Field(sa_type=sa.String(), nullable=False)
    expires_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
