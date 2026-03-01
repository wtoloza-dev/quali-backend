"""Update user route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.exceptions import UserAccessDeniedException
from ...infrastructure.dependencies import (
    GetUserUseCaseDependency,
    UpdateUserUseCaseDependency,
)
from ..mappers.user_mapper import UserMapper
from ..schemas import UpdateUserRequestSchema, UserPrivateResponseSchema


router = APIRouter()


@router.patch(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    description="Applies partial updates to an existing user. Only the user themselves can update their profile.",
)
async def handle_update_user_route(
    user_id: str,
    body: Annotated[UpdateUserRequestSchema, Body()],
    get_use_case: GetUserUseCaseDependency,
    update_use_case: UpdateUserUseCaseDependency,
    auth: CurrentUserDependency,
) -> UserPrivateResponseSchema:
    """Handle PATCH requests to update a user.

    Fetches the existing entity, applies only the non-None fields from
    the request body, then delegates to UpdateUserUseCase for persistence.

    Returns:
        UserPrivateResponseSchema: Updated user data.

    Raises:
        ForbiddenException: If the authenticated user is not the owner of the resource.
    """
    if auth.user_id != user_id:
        raise UserAccessDeniedException(user_id=user_id)
    existing = await get_use_case.execute(user_id)

    patch = body.model_dump(exclude_none=True)
    merged = existing.model_copy(update=patch)
    user = await update_use_case.execute(merged)
    return UserMapper.to_private_response(user)
