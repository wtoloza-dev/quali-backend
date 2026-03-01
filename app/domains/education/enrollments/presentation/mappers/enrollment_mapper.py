"""Enrollment entity-to-schema mapper."""

from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...domain.entities import EnrollmentEntity
from ..schemas.enrollment_response_schema import EnrollmentResponseSchema


class EnrollmentMapper:
    """Converts between EnrollmentEntity and enrollment response schemas."""

    @staticmethod
    def to_response(entity: EnrollmentEntity) -> EnrollmentResponseSchema:
        """Map an EnrollmentEntity to a full response schema.

        Args:
            entity: The enrollment entity to serialize.

        Returns:
            EnrollmentResponseSchema: Serialized enrollment data.
        """
        return EnrollmentResponseSchema(
            id=entity.id,
            user_id=entity.user_id,
            course_id=entity.course_id,
            company_id=entity.company_id,
            is_mandatory=entity.is_mandatory,
            status=entity.status,
            enrolled_at=entity.enrolled_at,
            completed_at=entity.completed_at,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )

    @staticmethod
    def to_paginated_response(
        items: list[EnrollmentEntity],
        total: int,
        params: PaginationParams,
    ) -> PaginatedResponse[EnrollmentResponseSchema]:
        """Map a list of enrollment entities to a paginated response.

        Args:
            items: The enrollment entities for the current page.
            total: Total number of records across all pages.
            params: Pagination parameters used to compute page metadata.

        Returns:
            Paginated envelope with enrollment schemas.
        """
        return PaginatedResponse(
            items=[EnrollmentMapper.to_response(e) for e in items],
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=params.pages(total),
        )
