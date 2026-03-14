"""Search user by email route handler."""

from fastapi import APIRouter, Query, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import SearchUserByEmailUseCaseDependency
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
    use_case: SearchUserByEmailUseCaseDependency,
    auth: CurrentUserDependency,
    email: str = Query(..., description="Exact email address to search for"),
) -> UserPrivateResponseSchema | None:
    """Handle GET requests to search a user by email.

    Args:
        use_case: Injected SearchUserByEmailUseCase.
        auth: Authenticated user context.
        email: The email address to search for.

    Returns:
        UserPrivateResponseSchema if found, null otherwise.
    """
    entity = await use_case.execute(email)
    if entity is None:
        return None
    return UserMapper.to_private_response(entity)
