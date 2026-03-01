"""Update lesson request schema."""

from pydantic import BaseModel, Field

from .content_block_schema import ContentBlockSchema


class UpdateLessonRequestSchema(BaseModel):
    """Input schema for the update lesson endpoint.

    Attributes:
        title: New lesson title.
        content: Replacement content block list. If provided, replaces all blocks.
        order: New position within the module.
    """

    title: str | None = None
    content: list[ContentBlockSchema] | None = None
    order: int | None = Field(default=None, ge=1)
