"""Module entity-to-schema mapper."""

from ...domain.entities import ModuleEntity
from ..schemas.module_response_schema import ModuleResponseSchema


class ModuleMapper:
    """Converts between ModuleEntity and module response schemas."""

    @staticmethod
    def to_response(entity: ModuleEntity) -> ModuleResponseSchema:
        """Map a ModuleEntity to a response schema.

        Args:
            entity: The module entity to serialize.

        Returns:
            ModuleResponseSchema: Serialized module data.
        """
        return ModuleResponseSchema(
            id=entity.id,
            course_id=entity.course_id,
            title=entity.title,
            order=entity.order,
            passing_score=entity.passing_score,
            max_attempts=entity.max_attempts,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
