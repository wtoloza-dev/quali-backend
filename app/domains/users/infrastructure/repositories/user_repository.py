"""User repository."""

from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel
from app.shared.services.encryption_service import decrypt, encrypt

from ...domain.entities import UserEntity
from ...domain.exceptions import UserEmailTakenException
from ..models.user_model import UserModel


class UserRepository:
    """Handles all database operations for user entities.

    Accepts and returns UserEntity objects. Never exposes UserModel
    outside this class. Owns all user query and persistence logic.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the repository with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: UserEntity) -> UserEntity:
        """Persist a new user entity and return the saved state.

        Args:
            entity: The user entity to persist.

        Returns:
            UserEntity: The persisted entity with DB-generated fields.
        """
        model = self._to_model(entity)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError:
            raise UserEmailTakenException(email=entity.email)
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Retrieve a user by its ULID identifier.

        Args:
            user_id: The ULID of the user.

        Returns:
            UserEntity if found, None otherwise.
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            UserEntity if found, None otherwise.
        """
        statement = select(UserModel).where(UserModel.email == email)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def update(self, entity: UserEntity) -> UserEntity:
        """Persist changes to an existing user entity.

        Args:
            entity: The user entity with updated fields.

        Returns:
            UserEntity: The updated entity after persistence.
        """
        statement = select(UserModel).where(UserModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.first_name = entity.first_name
        model.last_name = entity.last_name
        model.document_type = entity.document_type
        model.document_number = encrypt(entity.document_number) if entity.document_number else None
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, user_id: str, deleted_by: str) -> None:
        """Hard-delete a user and archive a tombstone snapshot for audit purposes.

        Args:
            user_id: The ULID of the user to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="user",
            entity_id=model.id,
            payload={
                "id": model.id,
                "first_name": model.first_name,
                "last_name": model.last_name,
                "email": model.email,
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

    async def list(self, page: int, page_size: int) -> tuple[list[UserEntity], int]:
        """Retrieve a paginated slice of users and the total count.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of UserEntity, total count).
        """
        count_stmt = select(func.count()).select_from(UserModel)
        total = (await self._session.exec(count_stmt)).one()
        stmt = select(UserModel).offset((page - 1) * page_size).limit(page_size)
        models = (await self._session.exec(stmt)).all()
        return [self._to_entity(m) for m in models], total

    @staticmethod
    def _to_entity(model: UserModel) -> UserEntity:
        """Map a UserModel ORM instance to a UserEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            UserEntity: The domain entity representation.
        """
        return UserEntity(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            document_type=model.document_type,
            document_number=decrypt(model.document_number) if model.document_number else None,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: UserEntity) -> UserModel:
        """Map a UserEntity to a UserModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            UserModel: The ORM model ready for persistence.
        """
        return UserModel(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            document_type=entity.document_type,
            document_number=encrypt(entity.document_number) if entity.document_number else None,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
