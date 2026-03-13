"""Access code repository port."""

from typing import Protocol

from ..entities import AccessCodeEntity


class AccessCodeRepositoryPort(Protocol):
    """Interface for the access code repository.

    Defined in the domain layer so use cases depend on this abstraction,
    not on the concrete SQLModel implementation.
    """

    async def save(self, entity: AccessCodeEntity) -> AccessCodeEntity:
        """Persist a new access code and return the saved state.

        Args:
            entity: The access code entity to persist.

        Returns:
            AccessCodeEntity: The persisted entity with DB-generated fields.
        """
        ...

    async def save_batch(
        self, entities: list[AccessCodeEntity]
    ) -> list[AccessCodeEntity]:
        """Persist multiple access codes and return the saved states.

        Args:
            entities: The access code entities to persist.

        Returns:
            List of persisted AccessCodeEntity instances.
        """
        ...

    async def get_by_code(self, code: str) -> AccessCodeEntity | None:
        """Retrieve an access code by its code string.

        Args:
            code: The access code string (QUALI-XXXX-XXXX format).

        Returns:
            AccessCodeEntity if found, None otherwise.
        """
        ...

    async def update(self, entity: AccessCodeEntity) -> AccessCodeEntity:
        """Persist changes to an existing access code entity.

        Args:
            entity: The access code entity with updated fields.

        Returns:
            AccessCodeEntity: The updated entity after persistence.
        """
        ...

    async def list_by_company(
        self,
        company_id: str,
        page: int,
        page_size: int,
    ) -> tuple[list[AccessCodeEntity], int]:
        """Return paginated access codes for all courses in a company.

        Args:
            company_id: The ULID of the company.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of AccessCodeEntity, total count).
        """
        ...
