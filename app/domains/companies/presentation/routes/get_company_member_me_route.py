"""Get current user's company membership route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency

from ...domain.exceptions import CompanyMemberNotFoundException
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
) -> CompanyMemberResponseSchema:
    """Handle GET requests to get the current user's membership in a company.

    Args:
        company_id: ULID of the company from the URL path.
        use_case: Injected GetCompanyMemberMeUseCase.
        auth: Authenticated user context.

    Returns:
        CompanyMemberResponseSchema: The membership record.

    Raises:
        CompanyMemberNotFoundException: If the user is not a member.
    """
    member = await use_case.execute(company_id, auth.user_id)
    if member is None:
        raise CompanyMemberNotFoundException(
            user_id=auth.user_id,
            company_id=company_id,
        )
    return CompanyMemberMapper.to_response(member)
