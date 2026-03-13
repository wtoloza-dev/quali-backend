"""Create module route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.entities import ModuleData
from ...infrastructure.dependencies import CreateModuleUseCaseDependency
from ..mappers.module_mapper import ModuleMapper
from ..schemas.create_module_schema import CreateModuleRequestSchema
from ..schemas.module_response_schema import ModuleResponseSchema


router = APIRouter()


@router.post(
    path="/{course_id}/modules",
    status_code=status.HTTP_201_CREATED,
    summary="Create a module",
    description="Adds a new module to a course. Only the owning company can add modules.",
)
async def handle_create_module_route(
    company_id: str,
    course_id: str,
    body: Annotated[CreateModuleRequestSchema, Body()],
    use_case: CreateModuleUseCaseDependency,
    auth: CurrentUserDependency,
) -> ModuleResponseSchema:
    """Handle POST requests to add a module to a course.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the parent course.
        body: Validated module creation request.
        use_case: Injected CreateModuleUseCase.
        auth: Authenticated user context.

    Returns:
        ModuleResponseSchema: The newly created module.
    """
    module = await use_case.execute(
        data=ModuleData(
            course_id=course_id,
            title=body.title,
            order=body.order,
            passing_score=body.passing_score,
            max_attempts=body.max_attempts,
        ),
        company_id=company_id,
        created_by=auth.user_id,
    )
    return ModuleMapper.to_response(module)
