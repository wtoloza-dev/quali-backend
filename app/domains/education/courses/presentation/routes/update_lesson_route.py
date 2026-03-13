"""Update lesson route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.exceptions import LessonNotFoundException
from ...infrastructure.dependencies import (
    LessonRepositoryDependency,
    UpdateLessonUseCaseDependency,
)
from ..mappers.lesson_mapper import LessonMapper
from ..schemas.lesson_response_schema import LessonResponseSchema
from ..schemas.update_lesson_schema import UpdateLessonRequestSchema


router = APIRouter()


@router.patch(
    path="/{course_id}/modules/{module_id}/lessons/{lesson_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a lesson",
    description="Partially updates a lesson within a module.",
)
async def handle_update_lesson_route(
    company_id: str,
    course_id: str,
    module_id: str,
    lesson_id: str,
    body: Annotated[UpdateLessonRequestSchema, Body()],
    lesson_repository: LessonRepositoryDependency,
    update_use_case: UpdateLessonUseCaseDependency,
    auth: CurrentUserDependency,
) -> LessonResponseSchema:
    """Handle PATCH requests to update a lesson.

    Fetches the existing lesson, merges provided fields, and persists.

    Args:
        company_id: ULID of the owning company resolved from the URL path.
        course_id: ULID of the parent course.
        module_id: ULID of the parent module.
        lesson_id: ULID of the lesson to update.
        body: Fields to update.
        lesson_repository: Injected lesson repository for lookup.
        update_use_case: Injected UpdateLessonUseCase.
        auth: Authenticated user context.

    Returns:
        LessonResponseSchema: The updated lesson.
    """
    existing = await lesson_repository.get_by_id(lesson_id)
    if existing is None or existing.module_id != module_id:
        raise LessonNotFoundException(lesson_id=lesson_id)

    patch = body.model_dump(exclude_none=True)
    merged = existing.model_copy(update=patch)

    updated = await update_use_case.execute(entity=merged, updated_by=auth.user_id)
    return LessonMapper.to_response(updated, has_access=True)
