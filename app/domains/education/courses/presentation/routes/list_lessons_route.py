"""List lessons route handler — public."""

from fastapi import APIRouter, status

from ...infrastructure.dependencies import ListLessonsUseCaseDependency
from ..schemas.lesson_summary_schema import LessonSummaryResponseSchema


router = APIRouter()


@router.get(
    path="/{course_id}/modules/{module_id}/lessons",
    status_code=status.HTTP_200_OK,
    summary="List lessons for a module",
    description=(
        "Returns all lessons for a module in order. "
        "Public — no authentication required. "
        "Only titles and order are exposed; lesson content is gated separately."
    ),
)
async def handle_list_lessons_route(
    module_id: str,
    use_case: ListLessonsUseCaseDependency,
) -> list[LessonSummaryResponseSchema]:
    """Handle GET requests to list lessons for a module.

    No auth required — lesson titles are public for discovery.
    Content access is enforced per-lesson via GetLessonRoute.

    Args:
        module_id: ULID of the parent module.
        use_case: Injected ListLessonsUseCase.

    Returns:
        list[LessonSummaryResponseSchema]: Ordered list of lesson summaries.
    """
    lessons = await use_case.execute(module_id=module_id)
    return [
        LessonSummaryResponseSchema(
            id=lesson.id,
            module_id=lesson.module_id,
            title=lesson.title,
            is_preview=lesson.is_preview,
            order=lesson.order,
            created_at=lesson.created_at,
        )
        for lesson in lessons
    ]
