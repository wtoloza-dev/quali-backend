"""User entity-to-schema mapper."""

from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...domain.entities import UserEntity
from ..schemas import UserPrivateResponseSchema, UserPublicResponseSchema


class UserMapper:
    """Converts between UserEntity and user response schemas.

    All methods are static. Contains no business logic — if a conversion
    requires a conditional for a business reason, that logic belongs
    in the service or entity instead.
    """

    @staticmethod
    def to_public_response(entity: UserEntity) -> UserPublicResponseSchema:
        """Map a UserEntity to a public response schema.

        Excludes PII fields such as email. Safe to return to other domains.

        Args:
            entity: The user entity to serialize.

        Returns:
            UserPublicResponseSchema: Serialized public user data.
        """
        return UserPublicResponseSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_private_response(entity: UserEntity) -> UserPrivateResponseSchema:
        """Map a UserEntity to a private response schema.

        Includes PII fields such as email and full audit data.

        Args:
            entity: The user entity to serialize.

        Returns:
            UserPrivateResponseSchema: Serialized full user data.
        """
        return UserPrivateResponseSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            document_type=entity.document_type,
            document_number=entity.document_number,
            is_superadmin=entity.is_superadmin,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )

    @staticmethod
    def to_paginated_response(
        items: list[UserEntity],
        total: int,
        params: PaginationParams,
    ) -> PaginatedResponse[UserPublicResponseSchema]:
        """Map a page of UserEntity objects to a paginated response envelope.

        Args:
            items: The slice of user entities for the current page.
            total: Total number of active users across all pages.
            params: Pagination parameters used to derive page metadata.

        Returns:
            PaginatedResponse[UserPublicResponseSchema]: Envelope with items
            and pagination metadata.
        """
        return PaginatedResponse(
            items=[UserMapper.to_public_response(e) for e in items],
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=params.pages(total),
        )
