"""Course entity-to-schema mapper."""

from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...domain.entities import CourseEntity
from ..schemas.course_public_response_schema import CoursePublicResponseSchema
from ..schemas.course_response_schema import CourseResponseSchema


class CourseMapper:
    """Converts between CourseEntity and course response schemas.

    Two response shapes:
    - to_public_response: safe for unauthenticated users (no company internals).
    - to_response: full data for authenticated users.
    """

    @staticmethod
    def to_public_response(entity: CourseEntity) -> CoursePublicResponseSchema:
        """Map a CourseEntity to a public response schema.

        Strips internal fields (company_id, audit timestamps) for
        unauthenticated discovery pages.

        Args:
            entity: The course entity to serialize.

        Returns:
            CoursePublicResponseSchema: Safe serialized course data.
        """
        return CoursePublicResponseSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            vertical=entity.vertical,
            regulatory_ref=entity.regulatory_ref,
            validity_days=entity.validity_days,
            passing_score=entity.passing_score,
            is_mandatory=entity.is_mandatory,
            visibility=entity.visibility,
            status=entity.status,
        )

    @staticmethod
    def to_response(entity: CourseEntity) -> CourseResponseSchema:
        """Map a CourseEntity to a full response schema for authenticated users.

        Args:
            entity: The course entity to serialize.

        Returns:
            CourseResponseSchema: Full serialized course data.
        """
        return CourseResponseSchema(
            id=entity.id,
            company_id=entity.company_id,
            title=entity.title,
            description=entity.description,
            vertical=entity.vertical,
            regulatory_ref=entity.regulatory_ref,
            validity_days=entity.validity_days,
            passing_score=entity.passing_score,
            max_attempts=entity.max_attempts,
            is_mandatory=entity.is_mandatory,
            visibility=entity.visibility,
            status=entity.status,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )

    @staticmethod
    def to_paginated_response(
        items: list[CourseEntity],
        total: int,
        params: PaginationParams,
        authenticated: bool = True,
    ) -> (
        PaginatedResponse[CourseResponseSchema]
        | PaginatedResponse[CoursePublicResponseSchema]
    ):
        """Map a list of course entities to a paginated response.

        Selects the appropriate schema based on whether the user is authenticated.

        Args:
            items: The course entities for the current page.
            total: Total number of records across all pages.
            params: Pagination parameters used to compute page metadata.
            authenticated: When False, returns public schemas only.

        Returns:
            Paginated envelope with the appropriate schema type.
        """
        if authenticated:
            return PaginatedResponse(
                items=[CourseMapper.to_response(e) for e in items],
                total=total,
                page=params.page,
                page_size=params.page_size,
                pages=params.pages(total),
            )
        return PaginatedResponse(
            items=[CourseMapper.to_public_response(e) for e in items],
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=params.pages(total),
        )
