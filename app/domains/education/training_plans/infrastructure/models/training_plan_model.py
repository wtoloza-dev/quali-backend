"""Training plan ORM model."""

import sqlalchemy as sa
from sqlmodel import Field

from app.shared.models.audit_model import AuditModel

from ...domain.enums import TrainingPlanStatus


class TrainingPlanModel(AuditModel, table=True):
    """SQLModel ORM model for the training_plans table.

    Attributes:
        __tablename__: Database table name.
        company_id: ULID of the owning company.
        year: Calendar year this plan covers.
        title: Human-readable title for the plan.
        status: Current lifecycle state.
    """

    __tablename__ = "training_plans"

    company_id: str = Field(nullable=False, index=True)
    year: int = Field(nullable=False)
    title: str = Field(nullable=False)
    status: TrainingPlanStatus = Field(
        default=TrainingPlanStatus.DRAFT,
        sa_type=sa.String(),
        nullable=False,
    )
