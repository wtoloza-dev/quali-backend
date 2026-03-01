"""Lesson response schema."""

from datetime import datetime

from pydantic import BaseModel

from .content_block_schema import ContentBlockSchema


class LessonResponseSchema(BaseModel):
    """Output schema for lesson endpoints.

    Attributes:
        id: ULID of the lesson.
        module_id: Parent module ULID.
        title: Lesson title.
        is_preview: True when content is free to view without access.
        is_locked: True when content was withheld because the requester has no access.
        content: Ordered list of content blocks. Empty list when locked.
        order: Position within the module.
        created_at: Creation timestamp.
        created_by: ULID of the creator.
        updated_at: Last update timestamp.
        updated_by: ULID of the last updater.
    """

    id: str
    module_id: str
    title: str
    is_preview: bool
    is_locked: bool
    content: list[ContentBlockSchema]
    order: int
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
