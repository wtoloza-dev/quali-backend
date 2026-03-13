"""Search user by email route handler."""

from fastapi import APIRouter, Query, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import UserRepositoryDependency
from ..mappers.user_mapper import UserMapper
from ..schemas import UserPrivateResponseSchema


router = APIRouter()


@router.get(
    path="/search",
    status_code=status.HTTP_200_OK,
    summary="Search user by email",
    description="Searches for a user by exact email match. Superadmin only.",
)
async def handle_search_user_by_email_route(
    email: str = Query(..., description="Exact email address to search for"),
    repository: UserRepositoryDependency = ...,
    auth: CurrentUserDependency = ...,
) -> UserPrivateResponseSchema | None:
    """Handle GET requests to search a user by email.

    Args:
        email: The email address to search for.
        repository: Injected user repository.
        auth: Authenticated user context.

    Returns:
        UserPrivateResponseSchema if found, null otherwise.
    """
    entity = await repository.get_by_email(email)
    if entity is None:
        return None
    return UserMapper.to_private_response(entity)
