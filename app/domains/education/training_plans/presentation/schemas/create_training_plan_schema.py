"""Create training plan request schema."""

from pydantic import BaseModel


class CreateTrainingPlanRequestSchema(BaseModel):
    """Request body for creating a training plan.

    Attributes:
        year: Calendar year this plan covers.
        title: Human-readable title for the plan.
    """

    year: int
    title: str
