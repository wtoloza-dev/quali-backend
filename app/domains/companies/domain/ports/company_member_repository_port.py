"""Company member repository port."""

from typing import Protocol

from ..entities import CompanyMemberEntity


class CompanyMemberRepositoryPort(Protocol):
    """Interface for the company member repository.

    Defined in the domain layer so the application layer depends on this
    abstraction, not on the concrete SQLModel implementation. The infrastructure
    layer provides the real implementation.
    """

    async def save(self, entity: CompanyMemberEntity) -> CompanyMemberEntity:
        """Persist a company member entity and return the saved state.

        Args:
            entity: The company member entity to persist.

        Returns:
            CompanyMemberEntity: The persisted entity with any DB-generated fields.
        """
        ...

    async def get_by_company_and_user(
        self, company_id: str, user_id: str
    ) -> CompanyMemberEntity | None:
        """Retrieve an active membership by company and user IDs.

        Args:
            company_id: The ULID of the company.
            user_id: The ULID of the user.

        Returns:
            CompanyMemberEntity if found, None otherwise.
        """
        ...

    async def get_by_company_id(self, company_id: str) -> list[CompanyMemberEntity]:
        """Retrieve all active members of a company.

        Args:
            company_id: The ULID of the company.

        Returns:
            List of active CompanyMemberEntity objects.
        """
        ...

    async def update(self, entity: CompanyMemberEntity) -> CompanyMemberEntity:
        """Persist changes to an existing company member entity.

        Args:
            entity: The company member entity with updated fields.

        Returns:
            CompanyMemberEntity: The updated entity after persistence.
        """
        ...

    async def delete(self, company_member_id: str, deleted_by: str) -> None:
        """Hard-delete a company membership and archive a tombstone snapshot for audit purposes.

        Args:
            company_member_id: The ULID of the membership record to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        ...
