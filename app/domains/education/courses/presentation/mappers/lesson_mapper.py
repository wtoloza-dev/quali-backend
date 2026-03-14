"""Lesson entity-to-schema mapper."""

from ...domain.entities import LessonEntity
from ..schemas.content_block_schema import ContentBlockSchema
from ..schemas.lesson_response_schema import LessonResponseSchema
from ..schemas.lesson_summary_schema import LessonSummaryResponseSchema


class LessonMapper:
    """Converts between LessonEntity and lesson response schemas.

    The mapper is responsible for access-aware serialization: it strips
    content blocks from lessons the requester is not allowed to read,
    and sets is_locked=True so the frontend can display a paywall.
    """

    @staticmethod
    def to_summary(entity: LessonEntity) -> LessonSummaryResponseSchema:
        """Map a LessonEntity to a lightweight summary without content.

        Args:
            entity: The lesson entity to serialize.

        Returns:
            LessonSummaryResponseSchema: Lightweight lesson representation.
        """
        return LessonSummaryResponseSchema(
            id=entity.id,
            module_id=entity.module_id,
            title=entity.title,
            is_preview=entity.is_preview,
            order=entity.order,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_response(entity: LessonEntity, has_access: bool) -> LessonResponseSchema:
        """Map a LessonEntity to a response schema, gating content by access.

        Content is included when the lesson is a preview OR the user has
        active access (enrollment, purchase, or subscription). Otherwise
        content is stripped and is_locked is set to True.

        Args:
            entity: The lesson entity to serialize.
            has_access: True if the requester has active course access.

        Returns:
            LessonResponseSchema: Serialized lesson, with content conditionally stripped.
        """
        unlocked = entity.is_preview or has_access
        content = (
            [ContentBlockSchema.model_validate(b.model_dump()) for b in entity.content]
            if unlocked
            else []
        )
        return LessonResponseSchema(
            id=entity.id,
            module_id=entity.module_id,
            title=entity.title,
            is_preview=entity.is_preview,
            is_locked=not unlocked,
            content=content,
            order=entity.order,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
