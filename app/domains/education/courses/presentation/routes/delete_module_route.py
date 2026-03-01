"""Delete module route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import DeleteModuleUseCaseDependency


router = APIRouter()


@router.delete(
    path="/{course_id}/modules/{module_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a module",
    description="Hard-deletes a module and all its lessons.",
)
async def handle_delete_module_route(
    company_id: str,
    course_id: str,
    module_id: str,
    use_case: DeleteModuleUseCaseDependency,
    auth: CurrentUserDependency,
) -> None:
    """Handle DELETE requests to remove a module.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the parent course.
        module_id: ULID of the module to delete.
        use_case: Injected DeleteModuleUseCase.
        auth: Authenticated user context.
    """
    await use_case.execute(
        course_id=course_id,
        module_id=module_id,
        company_id=company_id,
        deleted_by=auth.user_id,
    )
