"""Get lesson route handler — access-aware."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import OptionalCurrentUserDependency

from ...infrastructure.dependencies import (
    CheckCourseAccessUseCaseDependency,
    GetLessonUseCaseDependency,
)
from ..mappers.lesson_mapper import LessonMapper
from ..schemas.lesson_response_schema import LessonResponseSchema


router = APIRouter()


@router.get(
    path="/{course_id}/modules/{module_id}/lessons/{lesson_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a lesson",
    description=(
        "Returns a lesson. Content is included when: "
        "(1) the lesson is marked as preview, or "
        "(2) the authenticated user has active course access "
        "(enrollment, purchase, or subscription). "
        "Locked lessons return empty content and is_locked=true."
    ),
)
async def handle_get_lesson_route(
    course_id: str,
    module_id: str,  # noqa: ARG001 — URL context
    lesson_id: str,
    use_case: GetLessonUseCaseDependency,
    access_use_case: CheckCourseAccessUseCaseDependency,
    auth: OptionalCurrentUserDependency,
) -> LessonResponseSchema:
    """Handle GET requests to retrieve a lesson with access-aware content.

    Args:
        course_id: ULID of the parent course (used for access check).
        module_id: ULID of the parent module (URL context).
        lesson_id: ULID of the lesson to retrieve.
        use_case: Injected GetLessonUseCase.
        access_use_case: Injected CheckCourseAccessUseCase.
        auth: Authenticated user context, or None if unauthenticated.

    Returns:
        LessonResponseSchema: Lesson with content included or stripped.
    """
    lesson = await use_case.execute(lesson_id=lesson_id)

    has_access = lesson.is_preview or (
        auth is not None
        and await access_use_case.execute(
            user_id=auth.user_id,
            course_id=course_id,
        )
    )

    return LessonMapper.to_response(lesson, has_access=has_access)
