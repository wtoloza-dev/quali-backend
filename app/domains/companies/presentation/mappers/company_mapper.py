"""Company entity-to-schema mapper."""

from app.shared.schemas.pagination_schema import PaginatedResponse, PaginationParams

from ...domain.entities import CompanyEntity
from ..schemas import (
    CompanyPrivateResponseSchema,
    CompanyPublicResponseSchema,
    TaxResponseSchema,
)


class CompanyMapper:
    """Converts between CompanyEntity and company response schemas.

    All methods are static. Contains no business logic — if a conversion
    requires a conditional for a business reason, that logic belongs
    in the service or entity instead.
    """

    @staticmethod
    def to_public_response(entity: CompanyEntity) -> CompanyPublicResponseSchema:
        """Map a CompanyEntity to a public response schema.

        Excludes PII fields. Safe to return to unauthenticated users.

        Args:
            entity: The company entity to serialize.

        Returns:
            CompanyPublicResponseSchema: Serialized public company data.
        """
        return CompanyPublicResponseSchema(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            company_type=entity.company_type,
            country=entity.country,
            legal_name=entity.legal_name,
            logo_url=entity.logo_url,
        )

    @staticmethod
    def to_paginated_response(
        items: list[CompanyEntity],
        total: int,
        params: PaginationParams,
    ) -> PaginatedResponse[CompanyPublicResponseSchema]:
        """Map a list of company entities to a paginated public response.

        Args:
            items: The company entities for the current page.
            total: Total number of company records across all pages.
            params: Pagination parameters used to compute page metadata.

        Returns:
            PaginatedResponse[CompanyPublicResponseSchema]: Envelope with items
            and pagination metadata.
        """
        return PaginatedResponse(
            items=[CompanyMapper.to_public_response(e) for e in items],
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=params.pages(total),
        )

    @staticmethod
    def to_private_response(entity: CompanyEntity) -> CompanyPrivateResponseSchema:
        """Map a CompanyEntity to a private response schema.

        Includes PII fields. Only return to authenticated company members.

        Args:
            entity: The company entity to serialize.

        Returns:
            CompanyPrivateResponseSchema: Serialized full company data.
        """
        return CompanyPrivateResponseSchema(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            company_type=entity.company_type,
            email=entity.email,
            country=entity.country,
            tax=TaxResponseSchema(
                tax_type=entity.tax.tax_type,
                tax_id=entity.tax.tax_id,
            )
            if entity.tax
            else None,
            legal_name=entity.legal_name,
            logo_url=entity.logo_url,
        )
