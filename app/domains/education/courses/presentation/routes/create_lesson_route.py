"""Create lesson route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.entities import ContentBlock, LessonData
from ...infrastructure.dependencies import CreateLessonUseCaseDependency
from ..mappers.lesson_mapper import LessonMapper
from ..schemas.create_lesson_schema import CreateLessonRequestSchema
from ..schemas.lesson_response_schema import LessonResponseSchema


router = APIRouter()


@router.post(
    path="/{course_id}/modules/{module_id}/lessons",
    status_code=status.HTTP_201_CREATED,
    summary="Create a lesson",
    description="Adds a new lesson to a module.",
)
async def handle_create_lesson_route(
    company_id: str,
    course_id: str,  # noqa: ARG001 — kept for URL clarity
    module_id: str,
    body: Annotated[CreateLessonRequestSchema, Body()],
    use_case: CreateLessonUseCaseDependency,
    auth: CurrentUserDependency,
) -> LessonResponseSchema:
    """Handle POST requests to add a lesson to a module.

    Args:
        company_id: ULID of the owning company from the URL path.
        course_id: ULID of the parent course (URL context).
        module_id: ULID of the parent module.
        body: Validated lesson creation request.
        use_case: Injected CreateLessonUseCase.
        auth: Authenticated user context.

    Returns:
        LessonResponseSchema: The newly created lesson.
    """
    lesson = await use_case.execute(
        data=LessonData(
            module_id=module_id,
            title=body.title,
            content=[ContentBlock.model_validate(b.model_dump()) for b in body.content],
            order=body.order,
            is_preview=body.is_preview,
        ),
        company_id=company_id,
        created_by=auth.user_id,
    )
    return LessonMapper.to_response(lesson, has_access=True)
