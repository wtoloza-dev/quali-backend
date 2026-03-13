"""Generate access codes route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import GenerateAccessCodesUseCaseDependency
from ..mappers.access_code_mapper import AccessCodeMapper
from ..schemas.access_code_response_schema import AccessCodeResponseSchema
from ..schemas.generate_access_codes_schema import GenerateAccessCodesRequestSchema


router = APIRouter()


@router.post(
    path="/{course_id}/generate",
    status_code=status.HTTP_201_CREATED,
    summary="Generate access codes for a course",
)
async def handle_generate_access_codes_route(
    company_id: str,
    course_id: str,
    body: GenerateAccessCodesRequestSchema,
    use_case: GenerateAccessCodesUseCaseDependency,
    auth: CurrentUserDependency,
) -> list[AccessCodeResponseSchema]:
    """Handle POST requests to generate access codes for a course.

    Args:
        company_id: ULID of the company (from URL path).
        course_id: ULID of the course (from URL path).
        body: Request body with the quantity of codes to generate.
        use_case: Injected GenerateAccessCodesUseCase.
        auth: Authenticated user context.

    Returns:
        List of AccessCodeResponseSchema for the generated codes.
    """
    entities = await use_case.execute(
        course_id=course_id,
        quantity=body.quantity,
        created_by=auth.user_id,
    )
    return [AccessCodeMapper.to_response(e) for e in entities]
