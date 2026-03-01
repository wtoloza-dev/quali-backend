"""Get user route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.exceptions import UserAccessDeniedException
from ...infrastructure.dependencies import GetUserUseCaseDependency
from ..mappers.user_mapper import UserMapper
from ..schemas import UserPrivateResponseSchema


router = APIRouter()


@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a user by ID",
    description="Retrieves full user details by their ULID. Only the user themselves can access this.",
)
async def handle_get_user_route(
    user_id: str,
    use_case: GetUserUseCaseDependency,
    auth: CurrentUserDependency,
) -> UserPrivateResponseSchema:
    """Handle GET requests to retrieve a user by their ULID.

    Returns:
        UserPrivateResponseSchema: Full user data.

    Raises:
        ForbiddenException: If the authenticated user is not the owner of the resource.
    """
    if auth.user_id != user_id:
        raise UserAccessDeniedException(user_id=user_id)
    user = await use_case.execute(user_id)
    return UserMapper.to_private_response(user)
