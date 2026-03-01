"""Create lesson request schema."""

from pydantic import BaseModel, Field

from .content_block_schema import ContentBlockSchema


class CreateLessonRequestSchema(BaseModel):
    """Input schema for the create lesson endpoint.

    Attributes:
        title: Human-readable lesson title.
        content: Ordered list of content blocks.
        order: Position within the module (1-based).
        is_preview: When True, content is visible without purchase or enrollment.
    """

    title: str
    content: list[ContentBlockSchema] = []
    order: int = Field(ge=1)
    is_preview: bool = False
