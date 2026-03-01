"""Certificate entity-to-schema mapper."""

from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...domain.entities import CertificateEntity
from ..schemas import CertificatePrivateResponseSchema, CertificateVerifyResponseSchema


class CertificateMapper:
    """Converts between CertificateEntity and certificate response schemas.

    All methods are static. Contains no business logic — if a conversion
    requires a conditional for a business reason, that logic belongs
    in the service or entity instead.
    """

    @staticmethod
    def to_private_response(
        entity: CertificateEntity,
    ) -> CertificatePrivateResponseSchema:
        """Map a CertificateEntity to the private response schema.

        Args:
            entity: The domain entity to convert.

        Returns:
            CertificatePrivateResponseSchema: Full response for authenticated endpoints.
        """
        return CertificatePrivateResponseSchema(
            id=entity.id,
            company_id=entity.company_id,
            recipient_id=entity.recipient_id,
            title=entity.title,
            description=entity.description,
            token=entity.token,
            status=entity.status,
            issued_at=entity.issued_at,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
            revoked_by=entity.revoked_by,
            revoked_reason=entity.revoked_reason,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )

    @staticmethod
    def to_verify_response(
        entity: CertificateEntity,
    ) -> CertificateVerifyResponseSchema:
        """Map a CertificateEntity to the public verification response schema.

        Args:
            entity: The domain entity to convert.

        Returns:
            CertificateVerifyResponseSchema: Public response for QR scan verification.
        """
        return CertificateVerifyResponseSchema(
            id=entity.id,
            company_id=entity.company_id,
            recipient_id=entity.recipient_id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            issued_at=entity.issued_at,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
            revoked_reason=entity.revoked_reason,
        )

    @staticmethod
    def to_paginated_response(
        items: list[CertificateEntity],
        total: int,
        params: PaginationParams,
    ) -> PaginatedResponse[CertificatePrivateResponseSchema]:
        """Map a page of CertificateEntity items to a paginated response.

        Args:
            items: The certificate entities for the current page.
            total: Total number of certificates matching the query.
            params: The pagination parameters used for the query.

        Returns:
            PaginatedResponse[CertificatePrivateResponseSchema]: Paginated envelope.
        """
        return PaginatedResponse(
            items=[CertificateMapper.to_private_response(item) for item in items],
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=params.pages(total),
        )
