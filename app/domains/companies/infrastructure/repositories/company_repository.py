"""Company repository."""

from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import CompanyEntity
from ...domain.enums import TaxType
from ...domain.exceptions import CompanySlugTakenException
from ...domain.value_objects import Tax
from ..models.company_model import CompanyModel


class CompanyRepository:
    """Handles all database operations for company entities.

    Accepts and returns CompanyEntity objects. Never exposes
    CompanyModel outside this class. Owns all company
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

    async def save(self, entity: CompanyEntity) -> CompanyEntity:
        """Persist a new company entity and return the saved state.

        Args:
            entity: The company entity to persist.

        Returns:
            CompanyEntity: The persisted entity with DB-generated fields.
        """
        model = self._to_model(entity)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError:
            raise CompanySlugTakenException(slug=entity.slug)
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, company_id: str) -> CompanyEntity | None:
        """Retrieve a company by its ULID identifier.

        Args:
            company_id: The ULID of the company.

        Returns:
            CompanyEntity if found, None otherwise.
        """
        statement = select(CompanyModel).where(CompanyModel.id == company_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_slug(self, slug: str) -> CompanyEntity | None:
        """Retrieve a company by its unique slug.

        Args:
            slug: The URL-friendly unique identifier of the company.

        Returns:
            CompanyEntity if found, None otherwise.
        """
        statement = select(CompanyModel).where(CompanyModel.slug == slug)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def update(self, entity: CompanyEntity) -> CompanyEntity:
        """Persist changes to an existing company entity.

        Args:
            entity: The company entity with updated fields.

        Returns:
            CompanyEntity: The updated entity after persistence.
        """
        statement = select(CompanyModel).where(CompanyModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.name = entity.name
        model.company_type = entity.company_type
        model.email = entity.email
        model.country = entity.country
        model.legal_name = entity.legal_name
        model.logo_url = entity.logo_url
        model.tax_type = entity.tax.tax_type if entity.tax else None
        model.tax_id = entity.tax.tax_id if entity.tax else None
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, company_id: str, deleted_by: str) -> None:
        """Hard-delete a company and save a tombstone snapshot for audit purposes.

        Args:
            company_id: The ULID of the company to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        statement = select(CompanyModel).where(CompanyModel.id == company_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="company",
            entity_id=model.id,
            payload={
                "id": model.id,
                "name": model.name,
                "slug": model.slug,
                "company_type": model.company_type,
                "email": model.email,
                "country": model.country,
                "legal_name": model.legal_name,
                "logo_url": model.logo_url,
                "tax_type": model.tax_type,
                "tax_id": model.tax_id,
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

    async def list(self, page: int, page_size: int) -> tuple[list[CompanyEntity], int]:
        """Retrieve a paginated slice of companies and the total count.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of CompanyEntity, total count).
        """
        count_stmt = select(func.count()).select_from(CompanyModel)
        total = (await self._session.exec(count_stmt)).one()
        stmt = select(CompanyModel).offset((page - 1) * page_size).limit(page_size)
        models = (await self._session.exec(stmt)).all()
        return [self._to_entity(m) for m in models], total

    @staticmethod
    def _to_entity(model: CompanyModel) -> CompanyEntity:
        """Map a CompanyModel ORM instance to a CompanyEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            CompanyEntity: The domain entity representation.
        """
        tax = None
        if model.tax_type is not None and model.tax_id is not None:
            tax = Tax(tax_type=TaxType(model.tax_type), tax_id=model.tax_id)

        return CompanyEntity(
            id=model.id,
            name=model.name,
            slug=model.slug,
            company_type=model.company_type,
            email=model.email,
            country=model.country,
            tax=tax,
            legal_name=model.legal_name,
            logo_url=model.logo_url,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: CompanyEntity) -> CompanyModel:
        """Map a CompanyEntity to a CompanyModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            CompanyModel: The ORM model ready for persistence.
        """
        return CompanyModel(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            company_type=entity.company_type,
            email=entity.email,
            country=entity.country,
            tax_type=entity.tax.tax_type if entity.tax else None,
            tax_id=entity.tax.tax_id if entity.tax else None,
            legal_name=entity.legal_name,
            logo_url=entity.logo_url,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
