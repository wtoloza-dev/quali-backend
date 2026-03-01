"""List modules route handler — public."""

from fastapi import APIRouter, status

from ...infrastructure.dependencies import ListModulesUseCaseDependency
from ..mappers.module_mapper import ModuleMapper
from ..schemas.module_response_schema import ModuleResponseSchema


router = APIRouter()


@router.get(
    path="/{course_id}/modules",
    status_code=status.HTTP_200_OK,
    summary="List course modules",
    description=(
        "Returns all modules for a course in order. "
        "Public — no authentication required. "
        "Only titles and order are exposed; lesson content is gated separately."
    ),
)
async def handle_list_modules_route(
    course_id: str,
    use_case: ListModulesUseCaseDependency,
) -> list[ModuleResponseSchema]:
    """Handle GET requests to list modules for a course.

    No auth required — module structure is public for discovery.
    Lesson content access is enforced per-lesson.

    Args:
        course_id: ULID of the parent course.
        use_case: Injected ListModulesUseCase.

    Returns:
        list[ModuleResponseSchema]: Ordered list of modules.
    """
    modules = await use_case.execute(course_id=course_id)
    return [ModuleMapper.to_response(m) for m in modules]
