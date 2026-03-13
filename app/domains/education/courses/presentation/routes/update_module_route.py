"""Update module route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.exceptions import ModuleNotFoundException
from ...infrastructure.dependencies import (
    ModuleRepositoryDependency,
    UpdateModuleUseCaseDependency,
)
from ..mappers.module_mapper import ModuleMapper
from ..schemas.module_response_schema import ModuleResponseSchema
from ..schemas.update_module_schema import UpdateModuleRequestSchema


router = APIRouter()


@router.patch(
    path="/{course_id}/modules/{module_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a module",
    description="Partially updates a module within a course.",
)
async def handle_update_module_route(
    company_id: str,
    course_id: str,
    module_id: str,
    body: Annotated[UpdateModuleRequestSchema, Body()],
    module_repository: ModuleRepositoryDependency,
    update_use_case: UpdateModuleUseCaseDependency,
    auth: CurrentUserDependency,
) -> ModuleResponseSchema:
    """Handle PATCH requests to update a module.

    Fetches the existing module, merges provided fields, and persists.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the parent course.
        module_id: ULID of the module to update.
        body: Fields to update.
        module_repository: Injected module repository for lookup.
        update_use_case: Injected UpdateModuleUseCase.
        auth: Authenticated user context.

    Returns:
        ModuleResponseSchema: The updated module.
    """
    existing = await module_repository.get_by_id(module_id)
    if existing is None or existing.course_id != course_id:
        raise ModuleNotFoundException(module_id=module_id)

    patch = body.model_dump(exclude_none=True)
    merged = existing.model_copy(update=patch)

    updated = await update_use_case.execute(entity=merged, updated_by=auth.user_id)
    return ModuleMapper.to_response(updated)
