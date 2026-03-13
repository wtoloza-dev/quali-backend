"""Course repository."""

from datetime import UTC, datetime

from sqlmodel import func, or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import CourseEntity
from ...domain.enums import CourseVisibility
from ..models.course_model import CourseModel


class CourseRepository:
    """Handles all database operations for course entities.

    Accepts and returns CourseEntity objects. Never exposes
    CourseModel outside this class.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: CourseEntity) -> CourseEntity:
        """Persist a new course and return the saved state.

        Args:
            entity: The course entity to persist.

        Returns:
            CourseEntity: The persisted entity with DB-generated fields.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, course_id: str) -> CourseEntity | None:
        """Retrieve a course by ULID.

        Args:
            course_id: The ULID of the course.

        Returns:
            CourseEntity if found, None otherwise.
        """
        statement = select(CourseModel).where(CourseModel.id == course_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_id_and_company(
        self, course_id: str, company_id: str
    ) -> CourseEntity | None:
        """Retrieve a course only if it is owned by the given company.

        Args:
            course_id: The ULID of the course.
            company_id: The company that must own the course.

        Returns:
            CourseEntity if found and owned, None otherwise.
        """
        statement = select(CourseModel).where(
            CourseModel.id == course_id,
            CourseModel.company_id == company_id,
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def update(self, entity: CourseEntity) -> CourseEntity:
        """Persist changes to an existing course entity.

        Args:
            entity: The course entity with updated fields.

        Returns:
            CourseEntity: The updated entity after persistence.
        """
        statement = select(CourseModel).where(CourseModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.title = entity.title
        model.description = entity.description
        model.vertical = entity.vertical
        model.regulatory_ref = entity.regulatory_ref
        model.validity_days = entity.validity_days
        model.visibility = entity.visibility
        model.status = entity.status
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, course_id: str, deleted_by: str) -> None:
        """Hard-delete a course and archive a tombstone snapshot.

        Args:
            course_id: The ULID of the course to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        statement = select(CourseModel).where(CourseModel.id == course_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="course",
            entity_id=model.id,
            payload={
                "id": model.id,
                "company_id": model.company_id,
                "title": model.title,
                "vertical": model.vertical,
                "visibility": model.visibility,
                "status": model.status,
                "created_at": model.created_at.isoformat()
                if model.created_at
                else None,
                "created_by": model.created_by,
            },
            deleted_at=datetime.now(UTC),
            deleted_by=deleted_by,
        )
        self._session.add(tombstone)
        await self._session.delete(model)
        await self._session.flush()

    async def list(
        self,
        page: int,
        page_size: int,
        company_id: str,
    ) -> tuple[list[CourseEntity], int]:
        """Return paginated courses visible to the company.

        A course is visible when it is public OR owned by the company.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.
            company_id: The requesting company's ID.

        Returns:
            Tuple of (list of CourseEntity, total count).
        """
        visibility_filter = or_(
            CourseModel.visibility == CourseVisibility.PUBLIC,
            CourseModel.company_id == company_id,
        )

        count_stmt = (
            select(func.count()).select_from(CourseModel).where(visibility_filter)
        )
        total = (await self._session.exec(count_stmt)).one()

        stmt = (
            select(CourseModel)
            .where(visibility_filter)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        models = (await self._session.exec(stmt)).all()
        return [self._to_entity(m) for m in models], total

    @staticmethod
    def _to_entity(model: CourseModel) -> CourseEntity:
        """Map a CourseModel to a CourseEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            CourseEntity: The domain entity representation.
        """
        return CourseEntity(
            id=model.id,
            company_id=model.company_id,
            title=model.title,
            slug=model.slug,
            description=model.description,
            vertical=model.vertical,
            regulatory_ref=model.regulatory_ref,
            validity_days=model.validity_days,
            visibility=model.visibility,
            status=model.status,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: CourseEntity) -> CourseModel:
        """Map a CourseEntity to a CourseModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            CourseModel: The ORM model ready for persistence.
        """
        return CourseModel(
            id=entity.id,
            company_id=entity.company_id,
            title=entity.title,
            slug=entity.slug,
            description=entity.description,
            vertical=entity.vertical,
            regulatory_ref=entity.regulatory_ref,
            validity_days=entity.validity_days,
            visibility=entity.visibility,
            status=entity.status,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
