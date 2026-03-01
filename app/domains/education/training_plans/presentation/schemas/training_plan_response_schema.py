"""Training plan response schema."""

from datetime import datetime

from pydantic import BaseModel

from ...domain.enums import TrainingPlanStatus


class TrainingPlanResponseSchema(BaseModel):
    """Full training plan response.

    Attributes:
        id: ULID of the plan.
        company_id: ULID of the owning company.
        year: Calendar year this plan covers.
        title: Human-readable plan title.
        status: Current lifecycle state.
        created_at: Audit timestamp.
        created_by: ULID of the creator.
        updated_at: Audit timestamp.
        updated_by: ULID of the last updater.
    """

    id: str
    company_id: str
    year: int
    title: str
    status: TrainingPlanStatus
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
