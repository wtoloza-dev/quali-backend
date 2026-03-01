"""Create user route handler."""

from fastapi import APIRouter, Response, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.entities import UserData
from ...infrastructure.dependencies import (
    CreateUserUseCaseDependency,
    UserRepositoryDependency,
)
from ..mappers.user_mapper import UserMapper
from ..schemas import UserPrivateResponseSchema


router = APIRouter()


@router.post(
    path="/me",
    status_code=status.HTTP_201_CREATED,
    summary="Register current user profile",
    description=(
        "Creates the user profile for the authenticated Firebase user. "
        "Called once after the first login."
    ),
)
async def handle_create_user_route(
    auth: CurrentUserDependency,
    use_case: CreateUserUseCaseDependency,
    user_repo: UserRepositoryDependency,
    response: Response,
) -> UserPrivateResponseSchema:
    """Handle POST requests to create the authenticated user's profile.

    Args:
        auth: Authenticated Firebase user context.
        use_case: Injected CreateUserUseCase.
        user_repo: Injected UserRepository for duplicate checks.
        response: FastAPI response object to set status code.

    Returns:
        UserPrivateResponseSchema: The newly created user data.
    """
    existing = await user_repo.get_by_email(auth.email)
    if existing is not None:
        response.status_code = status.HTTP_200_OK
        return UserMapper.to_private_response(existing)

    user = await use_case.execute(
        UserData(
            first_name="",
            last_name="",
            email=auth.email,
        ),
        created_by=auth.user_id,
        user_id=auth.user_id,
    )
    return UserMapper.to_private_response(user)
