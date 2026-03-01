"""Course access domain entity."""

from datetime import datetime

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import AccessType


class CourseAccessData(BaseModel):
    """Lean data for granting course access.

    Attributes:
        user_id: The user receiving access.
        course_id: The course being unlocked.
        access_type: How access was granted (enrollment, purchase, subscription).
        expires_at: When access expires. None means permanent (e.g. à la carte purchase).
    """

    user_id: str
    course_id: str
    access_type: AccessType
    expires_at: datetime | None = None


class CourseAccessEntity(CourseAccessData, AuditEntity):
    """Full course access entity returned by the repository after persistence."""

    pass
