"""Create module request schema."""

from pydantic import BaseModel, Field


class CreateModuleRequestSchema(BaseModel):
    """Input schema for the create module endpoint.

    Attributes:
        title: Human-readable module title.
        order: Position within the course (1-based).
        passing_score: Minimum score (0–100) to pass this module's assessment.
        max_attempts: Maximum assessment attempts for this module.
    """

    title: str
    order: int = Field(ge=1)
    passing_score: int = Field(default=80, ge=0, le=100)
    max_attempts: int = Field(default=3, ge=1)
