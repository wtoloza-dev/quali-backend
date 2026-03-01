"""Training plan item response schema."""

from datetime import date, datetime

from pydantic import BaseModel


class TrainingPlanItemResponseSchema(BaseModel):
    """Full training plan item response.

    Attributes:
        id: ULID of the item.
        plan_id: ULID of the parent plan.
        course_id: ULID of the included course.
        target_role: Optional targeted role.
        scheduled_date: Optional target completion date.
        notes: Optional free-text notes.
        created_at: Audit timestamp.
        created_by: ULID of the creator.
    """

    id: str
    plan_id: str
    course_id: str
    target_role: str | None
    scheduled_date: date | None
    notes: str | None
    created_at: datetime
    created_by: str
