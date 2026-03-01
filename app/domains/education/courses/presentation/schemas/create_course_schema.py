"""Create course request schema."""

from pydantic import BaseModel, Field

from ...domain.enums import CourseVertical, CourseVisibility


class CreateCourseRequestSchema(BaseModel):
    """Input schema for the create course endpoint.

    Attributes:
        title: Human-readable course title.
        description: Optional longer description.
        vertical: Regulatory vertical (sst, food_quality, general).
        regulatory_ref: Optional regulatory clause reference.
        validity_days: Certificate validity in days. None means no expiry.
        passing_score: Minimum score (0–100) required to pass.
        max_attempts: Max assessment attempts before re-enrollment.
        is_mandatory: Whether completion is required for enrolled employees.
        visibility: PUBLIC (all companies) or PRIVATE (owning company only).
    """

    title: str
    description: str | None = None
    vertical: CourseVertical
    regulatory_ref: str | None = None
    validity_days: int | None = None
    passing_score: int = Field(default=80, ge=0, le=100)
    max_attempts: int = Field(default=3, ge=1)
    is_mandatory: bool = False
    visibility: CourseVisibility = CourseVisibility.PRIVATE
