"""Update module request schema."""

from pydantic import BaseModel, Field


class UpdateModuleRequestSchema(BaseModel):
    """Input schema for the update module endpoint.

    All fields are optional — only provided fields overwrite the existing values.

    Attributes:
        title: New module title.
        order: New position within the course.
        passing_score: New minimum passing score (0–100).
        max_attempts: New maximum assessment attempts.
    """

    title: str | None = None
    order: int | None = Field(default=None, ge=1)
    passing_score: int | None = Field(default=None, ge=0, le=100)
    max_attempts: int | None = Field(default=None, ge=1)
