"""Create module request schema."""

from pydantic import BaseModel, Field


class CreateModuleRequestSchema(BaseModel):
    """Input schema for the create module endpoint.

    Attributes:
        title: Human-readable module title.
        order: Position within the course (1-based).
    """

    title: str
    order: int = Field(ge=1)
