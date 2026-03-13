"""Get current user's company membership route handler."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.shared.auth.dependencies import CurrentUserDependency

from ...infrastructure.dependencies import GetCompanyMemberMeUseCaseDependency
from ..mappers.company_member_mapper import CompanyMemberMapper
from ..schemas.company_member_response_schema import CompanyMemberResponseSchema


router = APIRouter()


@router.get(
    path="/{company_id}/members/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user's membership",
    description="Returns the authenticated user's membership in a company, or 404 if not a member.",
    response_model=CompanyMemberResponseSchema,
)
async def handle_get_company_member_me_route(
    company_id: str,
    use_case: GetCompanyMemberMeUseCaseDependency,
    auth: CurrentUserDependency,
) -> CompanyMemberResponseSchema | JSONResponse:
    """Handle GET requests to get the current user's membership in a company.

    Returns:
        CompanyMemberResponseSchema: The membership record, or 404 if not a member.
    """
    member = await use_case.execute(company_id, auth.user_id)
    if member is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Not a member of this company."},
        )
    return CompanyMemberMapper.to_response(member)
