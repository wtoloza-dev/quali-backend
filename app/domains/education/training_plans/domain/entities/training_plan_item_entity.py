"""Training plan item domain entity."""

from datetime import date

from pydantic import BaseModel

from app.shared.entities import AuditEntity


class TrainingPlanItemData(BaseModel):
    """Input fields required to add an item to a training plan.

    Attributes:
        plan_id: ULID of the parent training plan.
        course_id: ULID of the course included in the plan.
        target_role: Optional role identifier this item targets.
        scheduled_date: Optional target completion date.
        notes: Optional free-text notes for this item.
    """

    plan_id: str
    course_id: str
    target_role: str | None = None
    scheduled_date: date | None = None
    notes: str | None = None


class TrainingPlanItemEntity(TrainingPlanItemData, AuditEntity):
    """Full persisted training plan item record."""
