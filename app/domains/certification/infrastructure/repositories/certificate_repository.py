"""Certificate repository."""

from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ...domain.entities import CertificateEntity
from ...domain.exceptions import CertificateTokenConflictException
from ..models.certificate_model import CertificateModel


class CertificateRepository:
    """Handles all database operations for certificate entities.

    Accepts and returns CertificateEntity objects. Never exposes
    CertificateModel outside this class. Owns all certificate
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

    async def save(self, entity: CertificateEntity) -> CertificateEntity:
        """Persist a new certificate entity and return the saved state.

        Args:
            entity: The certificate entity to persist.

        Returns:
            CertificateEntity: The persisted entity with DB-generated fields.
        """
        model = self._to_model(entity)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError:
            raise CertificateTokenConflictException(token=entity.token)
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, certificate_id: str) -> CertificateEntity | None:
        """Retrieve a certificate by its ULID identifier.

        Args:
            certificate_id: The ULID of the certificate.

        Returns:
            CertificateEntity if found, None otherwise.
        """
        statement = select(CertificateModel).where(
            CertificateModel.id == certificate_id
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_id_and_company(
        self, certificate_id: str, company_id: str
    ) -> CertificateEntity | None:
        """Retrieve a certificate scoped to a specific company.

        Args:
            certificate_id: The ULID of the certificate.
            company_id: The ULID of the owning company.

        Returns:
            CertificateEntity if found within the company, None otherwise.
        """
        statement = select(CertificateModel).where(
            CertificateModel.id == certificate_id,
            CertificateModel.company_id == company_id,
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_token(self, token: str) -> CertificateEntity | None:
        """Retrieve a certificate by its unique verification token.

        Args:
            token: The ULID token embedded in the QR code.

        Returns:
            CertificateEntity if found, None otherwise.
        """
        statement = select(CertificateModel).where(CertificateModel.token == token)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def update(self, entity: CertificateEntity) -> CertificateEntity:
        """Persist changes to an existing certificate entity.

        Args:
            entity: The certificate entity with updated fields.

        Returns:
            CertificateEntity: The updated entity after persistence.
        """
        statement = select(CertificateModel).where(CertificateModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.title = entity.title
        model.description = entity.description
        model.expires_at = entity.expires_at
        model.revoked_at = entity.revoked_at
        model.revoked_by = entity.revoked_by
        model.revoked_reason = entity.revoked_reason
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def list(
        self, company_id: str, page: int, page_size: int
    ) -> tuple[list[CertificateEntity], int]:
        """Retrieve a paginated slice of certificates for a company.

        Args:
            company_id: The ULID of the company whose certificates to list.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CertificateEntity, total count).
        """
        count_stmt = (
            select(func.count())
            .select_from(CertificateModel)
            .where(CertificateModel.company_id == company_id)
        )
        total = (await self._session.exec(count_stmt)).one()
        stmt = (
            select(CertificateModel)
            .where(CertificateModel.company_id == company_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        models = (await self._session.exec(stmt)).all()
        return [self._to_entity(m) for m in models], total

    async def list_by_recipient(
        self, recipient_id: str, page: int, page_size: int
    ) -> tuple[list[CertificateEntity], int]:
        """Retrieve a paginated slice of certificates for a recipient.

        Args:
            recipient_id: The Firebase UID of the certificate recipient.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CertificateEntity, total count).
        """
        count_stmt = (
            select(func.count())
            .select_from(CertificateModel)
            .where(CertificateModel.recipient_id == recipient_id)
        )
        total = (await self._session.exec(count_stmt)).one()
        stmt = (
            select(CertificateModel)
            .where(CertificateModel.recipient_id == recipient_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        models = (await self._session.exec(stmt)).all()
        return [self._to_entity(m) for m in models], total

    @staticmethod
    def _to_entity(model: CertificateModel) -> CertificateEntity:
        """Map a CertificateModel ORM instance to a CertificateEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            CertificateEntity: The domain entity representation.
        """
        return CertificateEntity(
            id=model.id,
            company_id=model.company_id,
            recipient_id=model.recipient_id,
            title=model.title,
            description=model.description,
            token=model.token,
            issued_at=model.issued_at,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
            revoked_by=model.revoked_by,
            revoked_reason=model.revoked_reason,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: CertificateEntity) -> CertificateModel:
        """Map a CertificateEntity to a CertificateModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            CertificateModel: The ORM model ready for persistence.
        """
        return CertificateModel(
            id=entity.id,
            company_id=entity.company_id,
            recipient_id=entity.recipient_id,
            title=entity.title,
            description=entity.description,
            token=entity.token,
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
