"""Course lesson domain entity."""

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import LessonContentType


class ContentBlock(BaseModel):
    """A single content block within a lesson.

    A lesson may contain multiple ordered blocks of mixed types
    (e.g. an intro text, then a video, then a downloadable PDF).

    Attributes:
        type: Discriminator — text, video, or file.
        order: Position of this block within the lesson (1-based).
        body: Rich text / HTML content. Only present when type is TEXT.
        url: Resource URL. Present for VIDEO and FILE types.
        provider: Video hosting provider (youtube, vimeo, hosted). VIDEO only.
        duration_seconds: Video duration hint for the UI. VIDEO only.
        filename: Original filename shown to the learner. FILE only.
    """

    type: LessonContentType
    order: int
    body: str | None = None
    url: str | None = None
    provider: str | None = None
    duration_seconds: int | None = None
    filename: str | None = None


class LessonData(BaseModel):
    """Lean lesson data used by use cases that create a lesson.

    Attributes:
        module_id: The module this lesson belongs to.
        title: Human-readable title of the lesson.
        content: Ordered list of content blocks that make up this lesson.
        order: Position of this lesson within the module (1-based).
        is_preview: When True, content is visible without purchase or enrollment.
    """

    module_id: str
    title: str
    content: list[ContentBlock] = []
    order: int
    is_preview: bool = False


class LessonEntity(LessonData, AuditEntity):
    """Full lesson entity returned by the repository after persistence."""

    pass
