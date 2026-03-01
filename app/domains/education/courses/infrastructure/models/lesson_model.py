"""Course lesson SQLModel ORM model."""

from typing import Any

from sqlalchemy import JSON
from sqlmodel import Field

from app.shared.models import AuditModel


class LessonModel(AuditModel, table=True):
    """SQLModel ORM representation of the course_lessons table.

    Lessons store content as an ordered JSON array of typed blocks.
    Each block carries a discriminator field (`type`) and only the
    fields relevant to that type.

    Attributes:
        __tablename__: Database table name.
        module_id: Parent module (indexed).
        title: Human-readable lesson title.
        content: Ordered list of content blocks (JSON column).
        order: Position within the module (1-based, ascending).
        is_preview: When True, content is visible without purchase or enrollment.
    """

    __tablename__ = "course_lessons"

    module_id: str = Field(nullable=False, index=True)
    title: str = Field(nullable=False)
    content: list[dict[str, Any]] = Field(
        default_factory=list,
        sa_type=JSON,
        nullable=False,
    )
    order: int = Field(nullable=False)
    is_preview: bool = Field(default=False, nullable=False)
