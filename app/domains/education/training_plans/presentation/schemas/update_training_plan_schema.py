"""Update training plan request schema."""

from pydantic import BaseModel

from ...domain.enums import TrainingPlanStatus


class UpdateTrainingPlanRequestSchema(BaseModel):
    """Request body for updating a training plan.

    Attributes:
        title: Updated plan title.
        status: Updated lifecycle status.
    """

    title: str | None = None
    status: TrainingPlanStatus | None = None
