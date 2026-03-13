"""Access code entity-to-schema mapper."""

from ...domain.entities import AccessCodeEntity
from ..schemas.access_code_response_schema import AccessCodeResponseSchema


class AccessCodeMapper:
    """Converts between AccessCodeEntity and access code response schemas."""

    @staticmethod
    def to_response(entity: AccessCodeEntity) -> AccessCodeResponseSchema:
        """Map an AccessCodeEntity to a full response schema.

        Args:
            entity: The access code entity to serialize.

        Returns:
            AccessCodeResponseSchema: Serialized access code data.
        """
        return AccessCodeResponseSchema(
            id=entity.id,
            code=entity.code,
            course_id=entity.course_id,
            is_redeemed=entity.is_redeemed,
            redeemed_by=entity.redeemed_by,
            redeemed_at=entity.redeemed_at,
            enrollment_id=entity.enrollment_id,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
