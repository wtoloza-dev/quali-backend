"""Company member repository."""

from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import CompanyMemberEntity
from ...domain.exceptions import CompanyMemberAlreadyExistsException
from ..models.company_member_model import CompanyMemberModel


class CompanyMemberRepository:
    """Handles all database operations for company member entities.

    Accepts and returns CompanyMemberEntity objects. Never exposes
    CompanyMemberModel outside this class. Owns all membership
    query and persistence logic.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the repository with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: CompanyMemberEntity) -> CompanyMemberEntity:
        """Persist a new company member entity and return the saved state.

        Args:
            entity: The company member entity to persist.

        Returns:
            CompanyMemberEntity: The persisted entity with DB-generated fields.

        Raises:
            CompanyMemberAlreadyExistsException: If the (company_id, user_id) pair
                violates the unique constraint (concurrent duplicate insert).
        """
        model = self._to_model(entity)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError:
            raise CompanyMemberAlreadyExistsException(
                user_id=entity.user_id, company_id=entity.company_id
            )
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_company_and_user(
        self, company_id: str, user_id: str
    ) -> CompanyMemberEntity | None:
        """Retrieve a membership by company and user IDs.

        Args:
            company_id: The ULID of the company.
            user_id: The ULID of the user.

        Returns:
            CompanyMemberEntity if found, None otherwise.
        """
        statement = select(CompanyMemberModel).where(
            CompanyMemberModel.company_id == company_id,
            CompanyMemberModel.user_id == user_id,
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_company_id(self, company_id: str) -> list[CompanyMemberEntity]:
        """Retrieve all members of a company.

        Args:
            company_id: The ULID of the company.

        Returns:
            List of CompanyMemberEntity objects.
        """
        statement = select(CompanyMemberModel).where(
            CompanyMemberModel.company_id == company_id,
        )
        result = await self._session.exec(statement)
        return [self._to_entity(model) for model in result.all()]

    async def delete(self, company_member_id: str, deleted_by: str) -> None:
        """Hard-delete a membership and save a tombstone snapshot for audit purposes.

        Args:
            company_member_id: The ULID of the membership record to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        statement = select(CompanyMemberModel).where(
            CompanyMemberModel.id == company_member_id
        )
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="company_member",
            entity_id=model.id,
            payload={
                "id": model.id,
                "company_id": model.company_id,
                "user_id": model.user_id,
                "role": model.role,
                "created_at": model.created_at.isoformat()
                if model.created_at
                else None,
                "created_by": model.created_by,
                "updated_at": model.updated_at.isoformat()
                if model.updated_at
                else None,
                "updated_by": model.updated_by,
            },
            deleted_at=datetime.now(UTC),
            deleted_by=deleted_by,
        )
        self._session.add(tombstone)
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_entity(model: CompanyMemberModel) -> CompanyMemberEntity:
        """Map a CompanyMemberModel ORM instance to a CompanyMemberEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            CompanyMemberEntity: The domain entity representation.
        """
        return CompanyMemberEntity(
            id=model.id,
            company_id=model.company_id,
            user_id=model.user_id,
            role=model.role,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: CompanyMemberEntity) -> CompanyMemberModel:
        """Map a CompanyMemberEntity to a CompanyMemberModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            CompanyMemberModel: The ORM model ready for persistence.
        """
        return CompanyMemberModel(
            id=entity.id,
            company_id=entity.company_id,
            user_id=entity.user_id,
            role=entity.role,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
