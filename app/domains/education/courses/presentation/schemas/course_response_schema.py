"""Course response schema."""

from datetime import datetime

from pydantic import BaseModel

from ...domain.enums import CourseStatus, CourseVertical, CourseVisibility


class CourseResponseSchema(BaseModel):
    """Output schema for course endpoints.

    Attributes:
        id: ULID of the course.
        company_id: Owning company.
        title: Course title.
        description: Optional description.
        vertical: Regulatory vertical.
        regulatory_ref: Optional regulatory clause reference.
        validity_days: Certificate validity in days.
        visibility: PUBLIC or PRIVATE.
        status: Lifecycle status (draft, published, archived).
        created_at: Creation timestamp.
        created_by: ULID of the creator.
        updated_at: Last update timestamp.
        updated_by: ULID of the last updater.
    """

    id: str
    company_id: str
    title: str
    slug: str
    description: str | None
    vertical: CourseVertical
    regulatory_ref: str | None
    validity_days: int | None
    visibility: CourseVisibility
    status: CourseStatus
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
