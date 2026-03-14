"""Redeem access code route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import RedeemAccessCodeUseCaseDependency
from ..mappers.access_code_mapper import AccessCodeMapper
from ..schemas.access_code_response_schema import AccessCodeResponseSchema
from ..schemas.redeem_access_code_schema import RedeemAccessCodeRequestSchema


router = APIRouter()


@router.post(
    path="/redeem",
    status_code=status.HTTP_201_CREATED,
    summary="Redeem an access code",
)
async def handle_redeem_access_code_route(
    company_id: str,
    body: RedeemAccessCodeRequestSchema,
    use_case: RedeemAccessCodeUseCaseDependency,
    auth: CurrentUserDependency,
) -> AccessCodeResponseSchema:
    """Handle POST requests to redeem an access code.

    Args:
        company_id: ULID of the company (from URL path).
        body: Request body with the access code to redeem.
        use_case: Injected RedeemAccessCodeUseCase.
        auth: Authenticated user context.

    Returns:
        AccessCodeResponseSchema: The redeemed access code.
    """
    entity = await use_case.execute(
        code=body.code,
        user_id=auth.user_id,
    )
    return AccessCodeMapper.to_response(entity)
