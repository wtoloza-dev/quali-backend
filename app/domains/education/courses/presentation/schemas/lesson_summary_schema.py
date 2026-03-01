"""Lesson summary schema — lightweight listing without content."""

from datetime import datetime

from pydantic import BaseModel


class LessonSummaryResponseSchema(BaseModel):
    """Lightweight lesson representation for listing endpoints.

    Omits content blocks to reduce payload size when listing
    all lessons in a module.

    Attributes:
        id: ULID of the lesson.
        module_id: Parent module ULID.
        title: Lesson title.
        is_preview: True when content is free to view without access.
        order: Position within the module.
        created_at: Creation timestamp.
    """

    id: str
    module_id: str
    title: str
    is_preview: bool
    order: int
    created_at: datetime
