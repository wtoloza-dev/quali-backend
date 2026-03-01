"""Training plan item ORM model."""

from datetime import date

from sqlalchemy import Date
from sqlmodel import Field

from app.shared.models.audit_model import AuditModel


class TrainingPlanItemModel(AuditModel, table=True):
    """SQLModel ORM model for the training_plan_items table.

    Attributes:
        __tablename__: Database table name.
        plan_id: ULID of the parent training plan.
        course_id: ULID of the course included in the plan.
        target_role: Optional role this item targets.
        scheduled_date: Optional target completion date.
        notes: Optional free-text notes.
    """

    __tablename__ = "training_plan_items"

    plan_id: str = Field(nullable=False, index=True)
    course_id: str = Field(nullable=False, index=True)
    target_role: str | None = Field(default=None, nullable=True)
    scheduled_date: date | None = Field(
        default=None,
        nullable=True,
        sa_type=Date(),
    )
    notes: str | None = Field(default=None, nullable=True)
