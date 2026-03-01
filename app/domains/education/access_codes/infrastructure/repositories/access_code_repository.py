"""Access code repository."""

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ...domain.entities import AccessCodeEntity
from ..models.access_code_model import AccessCodeModel


class AccessCodeRepository:
    """Handles all database operations for access code entities.

    Accepts and returns AccessCodeEntity objects. Never exposes AccessCodeModel
    outside this class.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the repository with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: AccessCodeEntity) -> AccessCodeEntity:
        """Persist a new access code and return the saved state.

        Args:
            entity: The access code entity to persist.

        Returns:
            AccessCodeEntity: The persisted entity with DB-generated fields.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def save_batch(
        self, entities: list[AccessCodeEntity]
    ) -> list[AccessCodeEntity]:
        """Persist multiple access codes and return the saved states.

        Args:
            entities: The access code entities to persist.

        Returns:
            List of persisted AccessCodeEntity instances.
        """
        models = [self._to_model(e) for e in entities]
        for model in models:
            self._session.add(model)
        await self._session.flush()
        for model in models:
            await self._session.refresh(model)
        return [self._to_entity(m) for m in models]

    async def get_by_code(self, code: str) -> AccessCodeEntity | None:
        """Retrieve an access code by its code string.

        Args:
            code: The access code string (QUALI-XXXX-XXXX format).

        Returns:
            AccessCodeEntity if found, None otherwise.
        """
        statement = select(AccessCodeModel).where(AccessCodeModel.code == code)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def update(self, entity: AccessCodeEntity) -> AccessCodeEntity:
        """Persist changes to an existing access code entity.

        Args:
            entity: The access code entity with updated fields.

        Returns:
            AccessCodeEntity: The updated entity after persistence.
        """
        statement = select(AccessCodeModel).where(AccessCodeModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.is_redeemed = entity.is_redeemed
        model.redeemed_by = entity.redeemed_by
        model.redeemed_at = entity.redeemed_at
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: AccessCodeModel) -> AccessCodeEntity:
        """Map an AccessCodeModel ORM instance to an AccessCodeEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            AccessCodeEntity: The domain entity representation.
        """
        return AccessCodeEntity(
            id=model.id,
            code=model.code,
            course_id=model.course_id,
            company_id=model.company_id,
            is_redeemed=model.is_redeemed,
            redeemed_by=model.redeemed_by,
            redeemed_at=model.redeemed_at,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: AccessCodeEntity) -> AccessCodeModel:
        """Map an AccessCodeEntity to an AccessCodeModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            AccessCodeModel: The ORM model ready for persistence.
        """
        return AccessCodeModel(
            id=entity.id,
            code=entity.code,
            course_id=entity.course_id,
            company_id=entity.company_id,
            is_redeemed=entity.is_redeemed,
            redeemed_by=entity.redeemed_by,
            redeemed_at=entity.redeemed_at,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
