"""Access code entity-to-schema mapper."""

from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

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

    @staticmethod
    def to_paginated_response(
        items: list[AccessCodeEntity],
        total: int,
        params: PaginationParams,
    ) -> PaginatedResponse[AccessCodeResponseSchema]:
        """Map a list of access code entities to a paginated response.

        Args:
            items: The access code entities for the current page.
            total: Total number of records across all pages.
            params: Pagination parameters used to compute page metadata.

        Returns:
            Paginated envelope with access code schemas.
        """
        return PaginatedResponse(
            items=[AccessCodeMapper.to_response(e) for e in items],
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=params.pages(total),
        )
