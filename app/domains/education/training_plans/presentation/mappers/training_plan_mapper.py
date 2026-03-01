"""Training plan entity-to-schema mapper."""

from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...domain.entities import TrainingPlanEntity, TrainingPlanItemEntity
from ..schemas.training_plan_item_response_schema import TrainingPlanItemResponseSchema
from ..schemas.training_plan_response_schema import TrainingPlanResponseSchema


class TrainingPlanMapper:
    """Converts between TrainingPlanEntity and response schemas."""

    @staticmethod
    def to_response(entity: TrainingPlanEntity) -> TrainingPlanResponseSchema:
        """Map a TrainingPlanEntity to a response schema.

        Args:
            entity: The training plan entity to serialize.

        Returns:
            TrainingPlanResponseSchema: Serialized plan data.
        """
        return TrainingPlanResponseSchema(
            id=entity.id,
            company_id=entity.company_id,
            year=entity.year,
            title=entity.title,
            status=entity.status,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )

    @staticmethod
    def item_to_response(
        entity: TrainingPlanItemEntity,
    ) -> TrainingPlanItemResponseSchema:
        """Map a TrainingPlanItemEntity to a response schema.

        Args:
            entity: The training plan item entity to serialize.

        Returns:
            TrainingPlanItemResponseSchema: Serialized item data.
        """
        return TrainingPlanItemResponseSchema(
            id=entity.id,
            plan_id=entity.plan_id,
            course_id=entity.course_id,
            target_role=entity.target_role,
            scheduled_date=entity.scheduled_date,
            notes=entity.notes,
            created_at=entity.created_at,
            created_by=entity.created_by,
        )

    @staticmethod
    def to_paginated_response(
        items: list[TrainingPlanEntity],
        total: int,
        params: PaginationParams,
    ) -> PaginatedResponse[TrainingPlanResponseSchema]:
        """Map a list of training plan entities to a paginated response.

        Args:
            items: The entities for the current page.
            total: Total number of records across all pages.
            params: Pagination parameters.

        Returns:
            Paginated envelope with training plan schemas.
        """
        return PaginatedResponse(
            items=[TrainingPlanMapper.to_response(e) for e in items],
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=params.pages(total),
        )
