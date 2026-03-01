"""Course domain entity."""

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import CourseStatus, CourseVertical, CourseVisibility


class CourseData(BaseModel):
    """Lean course data used by use cases that create or update a course.

    Attributes:
        company_id: Owning company. Quali itself is just another company.
        title: Human-readable title of the course.
        description: Optional longer description shown on the course card.
        vertical: Regulatory vertical the course belongs to.
        regulatory_ref: Optional regulatory clause reference (e.g. Res. 0312 art. 9).
        validity_days: How long the issued certificate remains valid. None = no expiry.
        passing_score: Minimum score (0–100) required to pass the assessment.
        max_attempts: Maximum number of assessment attempts before re-enrollment.
        is_mandatory: Whether completion is required for enrolled employees.
        visibility: PUBLIC (all companies) or PRIVATE (owning company only).
        status: Lifecycle status of the course.
    """

    company_id: str
    title: str
    description: str | None = None
    vertical: CourseVertical
    regulatory_ref: str | None = None
    validity_days: int | None = None
    passing_score: int = 80
    max_attempts: int = 3
    is_mandatory: bool = False
    visibility: CourseVisibility = CourseVisibility.PRIVATE
    status: CourseStatus = CourseStatus.DRAFT


class CourseEntity(CourseData, AuditEntity):
    """Full course entity returned by the repository after persistence.

    Combines domain fields from CourseData with audit fields from AuditEntity.
    """

    pass
