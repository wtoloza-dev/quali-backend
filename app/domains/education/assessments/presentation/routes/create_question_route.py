"""Create assessment question route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.entities import QuestionData
from ...infrastructure.dependencies import CreateQuestionUseCaseDependency
from ..mappers.question_mapper import QuestionMapper
from ..schemas.create_question_schema import CreateQuestionRequestSchema
from ..schemas.question_response_schema import QuestionResponseSchema


router = APIRouter()


@router.post(
    path="/{course_id}/questions",
    status_code=status.HTTP_201_CREATED,
    summary="Add a question to a course's question bank",
)
async def handle_create_question_route(
    company_id: str,
    course_id: str,
    body: CreateQuestionRequestSchema,
    use_case: CreateQuestionUseCaseDependency,
    auth: CurrentUserDependency,
) -> QuestionResponseSchema:
    """Handle POST requests to add a question to a course."""
    data = QuestionData(
        course_id=course_id,
        module_id=body.module_id,
        text=body.text,
        question_type=body.question_type,
        config=body.config,
        randomize=body.randomize,
        order=body.order,
    )
    entity = await use_case.execute(
        data=data,
        company_id=company_id,
        created_by=auth.user_id,
    )
    return QuestionMapper.to_response(entity)
