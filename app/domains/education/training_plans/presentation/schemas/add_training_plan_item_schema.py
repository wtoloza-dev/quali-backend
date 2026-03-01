"""Add training plan item request schema."""

from datetime import date

from pydantic import BaseModel


class AddTrainingPlanItemRequestSchema(BaseModel):
    """Request body for adding a course item to a training plan.

    Attributes:
        course_id: ULID of the course to include.
        target_role: Optional role identifier this item targets.
        scheduled_date: Optional target completion date.
        notes: Optional free-text notes.
    """

    course_id: str
    target_role: str | None = None
    scheduled_date: date | None = None
    notes: str | None = None
