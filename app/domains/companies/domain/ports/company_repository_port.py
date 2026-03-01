"""Company repository port."""

from typing import Protocol

from ..entities import CompanyEntity


class CompanyRepositoryPort(Protocol):
    """Interface for the company repository.

    Defined in the domain layer so the application layer depends on this
    abstraction, not on the concrete SQLModel implementation. The infrastructure
    layer provides the real implementation.
    """

    async def save(self, entity: CompanyEntity) -> CompanyEntity:
        """Persist a company entity and return the saved state.

        Args:
            entity: The company entity to persist.

        Returns:
            CompanyEntity: The persisted entity with any DB-generated fields.
        """
        ...

    async def get_by_id(self, company_id: str) -> CompanyEntity | None:
        """Retrieve a company by its ULID identifier.

        Args:
            company_id: The ULID of the company.

        Returns:
            CompanyEntity if found, None otherwise.
        """
        ...

    async def get_by_slug(self, slug: str) -> CompanyEntity | None:
        """Retrieve a company by its unique slug.

        Args:
            slug: The URL-friendly unique identifier of the company.

        Returns:
            CompanyEntity if found, None otherwise.
        """
        ...

    async def update(self, entity: CompanyEntity) -> CompanyEntity:
        """Persist changes to an existing company entity.

        Args:
            entity: The company entity with updated fields.

        Returns:
            CompanyEntity: The updated entity reflecting the persisted state.
        """
        ...

    async def delete(self, company_id: str, deleted_by: str) -> None:
        """Hard-delete a company and archive a tombstone snapshot for audit purposes.

        Args:
            company_id: The ULID of the company to delete.
            deleted_by: ID of the user performing the deletion.
        """
        ...

    async def list(self, page: int, page_size: int) -> tuple[list[CompanyEntity], int]:
        """Retrieve a paginated slice of companies and the total count.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CompanyEntity, total count).
        """
        ...
