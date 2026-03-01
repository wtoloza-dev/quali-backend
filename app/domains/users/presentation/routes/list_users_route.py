"""List users route handler."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListUsersUseCaseDependency
from ..mappers.user_mapper import UserMapper
from ..schemas.user_public_response_schema import UserPublicResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List users",
    description="Returns a paginated list of users.",
)
async def handle_list_users_route(
    pagination: Annotated[PaginationParams, Depends()],
    use_case: ListUsersUseCaseDependency,
    auth: CurrentUserDependency,
) -> PaginatedResponse[UserPublicResponseSchema]:
    """Handle GET requests to list users with pagination.

    Args:
        pagination: Query parameters controlling page number and page size.
        use_case: Injected use case that retrieves the paginated user slice.
        auth: Authenticated user context.

    Returns:
        PaginatedResponse[UserPublicResponseSchema]: Envelope containing the
        page of public user records and associated pagination metadata.
    """
    items, total = await use_case.execute(
        page=pagination.page,
        page_size=pagination.page_size,
    )
    return UserMapper.to_paginated_response(items=items, total=total, params=pagination)
