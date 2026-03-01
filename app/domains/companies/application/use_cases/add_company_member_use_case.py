"""Add company member use case."""

from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import CompanyMemberData, CompanyMemberEntity
from ...domain.exceptions import CompanyMemberAlreadyExistsException
from ...domain.ports import CompanyMemberRepositoryPort


class AddCompanyMemberUseCase:
    """Handles adding a user as a member of a company.

    Validates that the (company_id, user_id) pair is not already an active
    membership, constructs the entity, and persists it via the repository.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: CompanyMemberRepositoryPort) -> None:
        """Initialize the use case with its required dependencies.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self, data: CompanyMemberData, created_by: str
    ) -> CompanyMemberEntity:
        """Execute the add company member workflow.

        Args:
            data: Validated membership data from the presentation layer.
            created_by: ULID of the authenticated user performing the action.

        Returns:
            CompanyMemberEntity: The persisted membership entity.

        Raises:
            CompanyMemberAlreadyExistsException: If the user is already an active member of the company.
        """
        existing = await self._repository.get_by_company_and_user(
            company_id=data.company_id,
            user_id=data.user_id,
        )
        if existing:
            raise CompanyMemberAlreadyExistsException(
                user_id=data.user_id,
                company_id=data.company_id,
            )

        now = datetime.now(UTC)
        entity = CompanyMemberEntity(
            id=str(ULID()),
            company_id=data.company_id,
            user_id=data.user_id,
            role=data.role,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
