"""List certificates route handler."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.require_role import require_role
from app.shared.auth.role import Role
from app.shared.contracts import GetUserByIdDependency
from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...infrastructure.dependencies import ListCertificatesUseCaseDependency
from ..mappers.certificate_mapper import CertificateMapper
from ..schemas import CertificatePrivateResponseSchema


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List certificates for a company",
    description="Returns a paginated list of certificates issued by the company. Requires at least VIEWER role.",
)
async def handle_list_certificates_route(
    company_id: str,
    pagination: Annotated[PaginationParams, Depends()],
    use_case: ListCertificatesUseCaseDependency,
    get_user: GetUserByIdDependency,
    auth: Annotated[AuthContext, require_role(Role.VIEWER)],
) -> PaginatedResponse[CertificatePrivateResponseSchema]:
    """Handle GET requests to list certificates for a company.

    Enriches each certificate with the recipient's full name via the
    get_user_by_id contract.

    Args:
        company_id: ULID of the company, resolved from the URL path.
        pagination: Parsed page and page_size query parameters.
        use_case: Injected ListCertificatesUseCase.
        get_user: Cross-domain contract to look up user data.
        auth: Authenticated user context with at least VIEWER role.

    Returns:
        PaginatedResponse[CertificatePrivateResponseSchema]: Paginated certificate list.
    """
    items, total = await use_case.execute(
        company_id=company_id,
        page=pagination.page,
        page_size=pagination.page_size,
    )

    recipient_ids = {e.recipient_id for e in items}
    user_map = {}
    for uid in recipient_ids:
        user = await get_user(user_id=uid)
        if user:
            user_map[uid] = user

    response_items = []
    for entity in items:
        schema = CertificateMapper.to_private_response(entity)
        user = user_map.get(entity.recipient_id)
        if user:
            schema.recipient_name = f"{user.first_name} {user.last_name}".strip()
        response_items.append(schema)

    return PaginatedResponse(
        items=response_items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=pagination.pages(total),
    )
