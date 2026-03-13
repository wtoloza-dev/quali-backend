"""Update course request schema."""

from pydantic import BaseModel

from ...domain.enums import CourseVertical, CourseVisibility


class UpdateCourseRequestSchema(BaseModel):
    """Input schema for the update course endpoint.

    All fields are optional — only provided fields overwrite the existing values.

    Attributes:
        title: New course title.
        description: New description.
        vertical: New vertical.
        regulatory_ref: New regulatory reference.
        validity_days: New certificate validity in days.
        visibility: New visibility setting.
    """

    title: str | None = None
    description: str | None = None
    vertical: CourseVertical | None = None
    regulatory_ref: str | None = None
    validity_days: int | None = None
    visibility: CourseVisibility | None = None
