"""Create course request schema."""

from pydantic import BaseModel

from ...domain.enums import CourseVertical, CourseVisibility


class CreateCourseRequestSchema(BaseModel):
    """Input schema for the create course endpoint.

    Attributes:
        title: Human-readable course title.
        description: Optional longer description.
        vertical: Regulatory vertical (sst, food_quality, general).
        regulatory_ref: Optional regulatory clause reference.
        validity_days: Certificate validity in days. None means no expiry.
        visibility: PUBLIC (all companies) or PRIVATE (owning company only).
    """

    title: str
    description: str | None = None
    vertical: CourseVertical
    regulatory_ref: str | None = None
    validity_days: int | None = None
    visibility: CourseVisibility = CourseVisibility.PRIVATE
