"""Delete user route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.exceptions import UserAccessDeniedException
from ...infrastructure.dependencies import DeleteUserUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Permanently deletes a user. Only the user themselves can delete their account.",
)
async def handle_delete_user_route(
    user_id: str,
    use_case: DeleteUserUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle DELETE requests to permanently delete a user.

    Returns:
        None: 204 No Content on success.

    Raises:
        ForbiddenException: If the authenticated user is not the owner of the resource.
    """
    if auth.user_id != user_id:
        raise UserAccessDeniedException(user_id=user_id)
    await use_case.execute(
        user_id=user_id,
        deleted_by=auth.user_id,
    )
