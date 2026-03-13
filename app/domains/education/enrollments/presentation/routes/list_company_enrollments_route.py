"""List company enrollments route handler."""

from typing import Annotated

from fastapi import APIRouter, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role
from app.shared.contracts import GetUserByIdDependency
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListCompanyEnrollmentsUseCaseDependency
from ..mappers.enrollment_mapper import EnrollmentMapper
from ..schemas.enrollment_response_schema import EnrollmentResponseSchema


router = APIRouter()


@router.get(
    path="/all",
    status_code=status.HTTP_200_OK,
    summary="List all enrollments for a company",
)
async def handle_list_company_enrollments_route(
    company_id: str,
    use_case: ListCompanyEnrollmentsUseCaseDependency,
    get_user: GetUserByIdDependency,
    auth: Annotated[AuthContext, require_role(Role.ADMIN)],
    params: PaginationParams = PaginationParams(),
) -> PaginatedResponse[EnrollmentResponseSchema]:
    """Handle GET requests to list all enrollments for a company.

    Enriches each enrollment with user info (email, first_name, last_name)
    via the get_user_by_id contract.

    Args:
        company_id: ULID of the company from the URL path.
        use_case: Injected ListCompanyEnrollmentsUseCase.
        get_user: Cross-domain contract to look up user data.
        auth: Authenticated user context with ADMIN+ role.
        params: Pagination parameters.

    Returns:
        PaginatedResponse[EnrollmentResponseSchema]: Paginated enrollment list.
    """
    items, total = await use_case.execute(
        company_id=company_id,
        params=params,
    )

    # Enrich with user data
    user_ids = {e.user_id for e in items}
    user_map = {}
    for uid in user_ids:
        user = await get_user(user_id=uid)
        if user:
            user_map[uid] = user

    response_items = []
    for entity in items:
        schema = EnrollmentMapper.to_response(entity)
        user = user_map.get(entity.user_id)
        if user:
            schema.user_email = user.email
            schema.user_first_name = user.first_name
            schema.user_last_name = user.last_name
        response_items.append(schema)

    return PaginatedResponse(
        items=response_items,
        total=total,
        page=params.page,
        page_size=params.page_size,
        pages=params.pages(total),
    )
