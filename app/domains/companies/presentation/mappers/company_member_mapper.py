"""Company member entity-to-schema mapper."""

from ...domain.entities import CompanyMemberEntity
from ..schemas.company_member_response_schema import CompanyMemberResponseSchema


class CompanyMemberMapper:
    """Converts between CompanyMemberEntity and company member response schemas.

    All methods are static. Contains no business logic.
    """

    @staticmethod
    def to_response(entity: CompanyMemberEntity) -> CompanyMemberResponseSchema:
        """Map a CompanyMemberEntity to a response schema.

        Args:
            entity: The company member entity to serialize.

        Returns:
            CompanyMemberResponseSchema: Serialized membership data.
        """
        return CompanyMemberResponseSchema(
            id=entity.id,
            company_id=entity.company_id,
            user_id=entity.user_id,
            role=entity.role,
            created_at=entity.created_at,
            created_by=entity.created_by,
        )
