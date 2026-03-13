"""Module response schema."""

from datetime import datetime

from pydantic import BaseModel


class ModuleResponseSchema(BaseModel):
    """Output schema for module endpoints.

    Attributes:
        id: ULID of the module.
        course_id: Parent course ULID.
        title: Module title.
        order: Position within the course.
        passing_score: Minimum score (0–100) to pass this module's assessment.
        max_attempts: Maximum assessment attempts for this module.
        created_at: Creation timestamp.
        created_by: ULID of the creator.
        updated_at: Last update timestamp.
        updated_by: ULID of the last updater.
    """

    id: str
    course_id: str
    title: str
    order: int
    passing_score: int
    max_attempts: int
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
