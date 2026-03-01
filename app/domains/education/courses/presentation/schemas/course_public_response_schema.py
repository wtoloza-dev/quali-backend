"""Course public response schema (unauthenticated)."""

from pydantic import BaseModel

from ...domain.enums import CourseStatus, CourseVertical, CourseVisibility


class CoursePublicResponseSchema(BaseModel):
    """Safe course representation for unauthenticated users.

    Exposes enough for marketing/discovery pages without leaking
    internal company metadata.

    Attributes:
        id: ULID of the course.
        title: Course title.
        description: Optional description.
        vertical: Regulatory vertical.
        regulatory_ref: Optional regulatory clause reference.
        validity_days: Certificate validity in days.
        passing_score: Minimum passing score.
        is_mandatory: Whether completion is mandatory.
        visibility: PUBLIC or PRIVATE.
        status: Lifecycle status.
    """

    id: str
    title: str
    description: str | None
    vertical: CourseVertical
    regulatory_ref: str | None
    validity_days: int | None
    passing_score: int
    is_mandatory: bool
    visibility: CourseVisibility
    status: CourseStatus
