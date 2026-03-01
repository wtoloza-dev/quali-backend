"""Training plan domain entity."""

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import TrainingPlanStatus


class TrainingPlanData(BaseModel):
    """Input fields required to create a training plan.

    Attributes:
        company_id: ULID of the company this plan belongs to.
        year: Calendar year this plan covers (e.g. 2026).
        title: Human-readable title for the plan.
    """

    company_id: str
    year: int
    title: str


class TrainingPlanEntity(TrainingPlanData, AuditEntity):
    """Full persisted training plan record.

    Attributes:
        status: Current lifecycle state of the plan.
    """

    status: TrainingPlanStatus = TrainingPlanStatus.DRAFT
