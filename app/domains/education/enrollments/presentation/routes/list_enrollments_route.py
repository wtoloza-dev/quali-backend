"""List enrollments route handler."""

from fastapi import APIRouter, status

from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListEnrollmentsUseCaseDependency
from ..mappers.enrollment_mapper import EnrollmentMapper
from ..schemas.enrollment_response_schema import EnrollmentResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List enrollments for a company",
)
async def handle_list_enrollments_route(
    company_id: str,
    use_case: ListEnrollmentsUseCaseDependency,
    auth: CurrentUserDependency,
    params: PaginationParams = PaginationParams(),
) -> PaginatedResponse[EnrollmentResponseSchema]:
    """Handle GET requests to list enrollments for the authenticated user.

    Args:
        company_id: ULID of the company (from URL path).
        use_case: Injected ListEnrollmentsUseCase.
        auth: Authenticated user context.
        params: Pagination parameters.

    Returns:
        PaginatedResponse[EnrollmentResponseSchema]: Paginated enrollment list.
    """
    items, total = await use_case.execute(
        company_id=company_id,
        user_id=auth.user_id,
        params=params,
    )
    return EnrollmentMapper.to_paginated_response(items, total, params)
