"""Current user profile routes (GET/PATCH /users/me)."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.contracts import (
    CertificateListContractResult,
    ListCertificatesByRecipientDependency,
)
from app.shared.exceptions import UnprocessableException
from app.shared.schemas.pagination_schema import PaginationParams

from ...infrastructure.dependencies import (
    GetUserUseCaseDependency,
    UpdateUserUseCaseDependency,
)
from ..mappers.user_mapper import UserMapper
from ..schemas import UpdateUserRequestSchema, UserPrivateResponseSchema


router = APIRouter()

# Fields that become immutable once set (non-empty).
_LOCKED_FIELDS = ("first_name", "last_name", "document_type", "document_number")


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Returns the authenticated user's profile using their Firebase UID.",
)
async def handle_get_me_route(
    use_case: GetUserUseCaseDependency,
    auth: CurrentUserDependency,
) -> UserPrivateResponseSchema:
    """Return the authenticated user's profile."""
    user = await use_case.execute(auth.user_id)
    return UserMapper.to_private_response(user)


@router.patch(
    path="/me",
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
    description="Updates the authenticated user's profile. Name and document fields can only be set once.",
)
async def handle_update_me_route(
    body: Annotated[UpdateUserRequestSchema, Body()],
    get_use_case: GetUserUseCaseDependency,
    update_use_case: UpdateUserUseCaseDependency,
    auth: CurrentUserDependency,
) -> UserPrivateResponseSchema:
    """Update the authenticated user's profile with partial data."""
    existing = await get_use_case.execute(auth.user_id)
    patch = body.model_dump(exclude_none=True)

    # Reject changes to fields that are already set to a different value.
    locked = [
        f for f in _LOCKED_FIELDS
        if f in patch and getattr(existing, f, None) and patch[f] != getattr(existing, f)
    ]
    if locked:
        raise UnprocessableException(
            message=f"Los campos {', '.join(locked)} ya fueron establecidos y no se pueden modificar.",
            error_code="FIELDS_LOCKED",
        )

    merged = existing.model_copy(update=patch)
    merged.updated_by = auth.user_id

    user = await update_use_case.execute(merged)
    return UserMapper.to_private_response(user)


@router.get(
    path="/me/certificates",
    status_code=status.HTTP_200_OK,
    summary="Get current user certificates",
    description="Returns a paginated list of certificates issued to the authenticated user.",
)
async def handle_list_my_certificates_route(
    pagination: Annotated[PaginationParams, Depends()],
    list_certificates: ListCertificatesByRecipientDependency,
    auth: CurrentUserDependency,
) -> CertificateListContractResult:
    """Return a paginated list of certificates for the authenticated user."""
    return await list_certificates(
        recipient_id=auth.user_id,
        page=pagination.page,
        page_size=pagination.page_size,
    )
