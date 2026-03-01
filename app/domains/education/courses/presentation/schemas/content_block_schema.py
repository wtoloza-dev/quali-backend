"""Content block request/response schema."""

from pydantic import BaseModel

from ...domain.enums import LessonContentType


class ContentBlockSchema(BaseModel):
    """Schema for a single lesson content block.

    Used in both request (create/update lesson) and response bodies.

    Attributes:
        type: Discriminator — text, video, or file.
        order: Position within the lesson (1-based).
        body: Rich text / HTML. Required when type is TEXT.
        url: Resource URL. Required for VIDEO and FILE.
        provider: Video provider (youtube, vimeo, hosted). VIDEO only.
        duration_seconds: Duration hint for the player. VIDEO only.
        filename: Original filename shown to the learner. FILE only.
    """

    type: LessonContentType
    order: int
    body: str | None = None
    url: str | None = None
    provider: str | None = None
    duration_seconds: int | None = None
    filename: str | None = None
