"""Submit assessment attempt route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.entities import AnswerEntry, AttemptData
from ...infrastructure.dependencies import SubmitAttemptUseCaseDependency
from ..mappers.attempt_mapper import AttemptMapper
from ..schemas.attempt_response_schema import AttemptResponseSchema
from ..schemas.submit_attempt_schema import SubmitAttemptRequestSchema


router = APIRouter()


@router.post(
    path="/{enrollment_id}/attempts",
    status_code=status.HTTP_201_CREATED,
    summary="Submit an assessment attempt",
    description=(
        "Scores the submitted answers against the course question bank. "
        "Advances the enrollment to 'in_progress', 'completed', or 'failed' "
        "based on the score and remaining attempts."
    ),
)
async def handle_submit_attempt_route(
    enrollment_id: str,
    body: SubmitAttemptRequestSchema,
    use_case: SubmitAttemptUseCaseDependency,
    auth: CurrentUserDependency,
) -> AttemptResponseSchema:
    """Handle POST requests to submit an assessment attempt.

    Args:
        enrollment_id: ULID of the enrollment (from URL path).
        body: Submitted answers for all questions.
        use_case: Injected SubmitAttemptUseCase.
        auth: Authenticated user context.

    Returns:
        AttemptResponseSchema: The scored attempt with pass/fail result.
    """
    data = AttemptData(
        enrollment_id=enrollment_id,
        module_id=body.module_id,
        answers=[
            AnswerEntry(
                question_id=a.question_id,
                selected_indices=a.selected_indices,
                found_words=a.found_words,
                cell_answers=a.cell_answers,
            )
            for a in body.answers
        ],
    )
    entity = await use_case.execute(data=data, submitted_by=auth.user_id)
    return AttemptMapper.to_response(entity)
