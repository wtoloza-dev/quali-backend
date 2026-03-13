"""Enrollment repository."""

from datetime import UTC, datetime

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import EnrollmentEntity
from ...domain.enums import EnrollmentStatus
from ..models.enrollment_model import EnrollmentModel


class EnrollmentRepository:
    """Handles all database operations for enrollment entities.

    Accepts and returns EnrollmentEntity objects. Never exposes EnrollmentModel
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

    async def save(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        """Persist a new enrollment and return the saved state.

        Args:
            entity: The enrollment entity to persist.

        Returns:
            EnrollmentEntity: The persisted entity with DB-generated fields.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, enrollment_id: str) -> EnrollmentEntity | None:
        """Retrieve an enrollment by its ULID.

        Args:
            enrollment_id: The ULID of the enrollment.

        Returns:
            EnrollmentEntity if found, None otherwise.
        """
        statement = select(EnrollmentModel).where(EnrollmentModel.id == enrollment_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_by_user_and_course(
        self, user_id: str, course_id: str
    ) -> EnrollmentEntity | None:
        """Return any enrollment for a user+course pair regardless of status.

        Args:
            user_id: The ULID of the user.
            course_id: The ULID of the course.

        Returns:
            EnrollmentEntity if found, None otherwise.
        """
        statement = select(EnrollmentModel).where(
            EnrollmentModel.user_id == user_id,
            EnrollmentModel.course_id == course_id,
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def get_active_enrollment(
        self, user_id: str, course_id: str
    ) -> EnrollmentEntity | None:
        """Return an active (not_started or in_progress) enrollment.

        Args:
            user_id: The ULID of the user.
            course_id: The ULID of the course.

        Returns:
            EnrollmentEntity if found, None otherwise.
        """
        statement = select(EnrollmentModel).where(
            EnrollmentModel.user_id == user_id,
            EnrollmentModel.course_id == course_id,
            EnrollmentModel.status.in_(  # type: ignore[union-attr]
                [EnrollmentStatus.NOT_STARTED, EnrollmentStatus.IN_PROGRESS]
            ),
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def update(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        """Persist changes to an existing enrollment.

        Args:
            entity: The enrollment entity with updated fields.

        Returns:
            EnrollmentEntity: The updated entity after persistence.
        """
        statement = select(EnrollmentModel).where(EnrollmentModel.id == entity.id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return entity

        model.status = entity.status
        model.access_type = entity.access_type
        model.completed_at = entity.completed_at
        model.start_date = entity.start_date
        model.end_date = entity.end_date
        model.updated_by = entity.updated_by

        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, enrollment_id: str, deleted_by: str) -> None:
        """Hard-delete an enrollment and archive a tombstone snapshot.

        Args:
            enrollment_id: The ULID of the enrollment to delete.
            deleted_by: ID of the actor performing the deletion.
        """
        statement = select(EnrollmentModel).where(EnrollmentModel.id == enrollment_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return

        tombstone = EntityTombstoneModel(
            entity_type="enrollment",
            entity_id=model.id,
            payload={
                "id": model.id,
                "user_id": model.user_id,
                "course_id": model.course_id,
                "is_mandatory": model.is_mandatory,
                "status": model.status,
                "access_type": model.access_type,
                "enrolled_at": model.enrolled_at.isoformat()
                if model.enrolled_at
                else None,
                "completed_at": model.completed_at.isoformat()
                if model.completed_at
                else None,
                "start_date": model.start_date.isoformat()
                if model.start_date
                else None,
                "end_date": model.end_date.isoformat() if model.end_date else None,
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

    async def list_by_user(
        self,
        user_id: str,
        page: int,
        page_size: int,
    ) -> tuple[list[EnrollmentEntity], int]:
        """Return a paginated slice of enrollments for a user.

        Args:
            user_id: ULID of the user whose enrollments to return.
            page: 1-based page number.
            page_size: Number of items per page.

        Returns:
            Tuple of (list of EnrollmentEntity, total count).
        """
        count_stmt = (
            select(func.count())
            .select_from(EnrollmentModel)
            .where(EnrollmentModel.user_id == user_id)
        )
        total = (await self._session.exec(count_stmt)).one()

        stmt = (
            select(EnrollmentModel)
            .where(EnrollmentModel.user_id == user_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        models = (await self._session.exec(stmt)).all()
        return [self._to_entity(m) for m in models], total

    @staticmethod
    def _to_entity(model: EnrollmentModel) -> EnrollmentEntity:
        """Map an EnrollmentModel ORM instance to an EnrollmentEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            EnrollmentEntity: The domain entity representation.
        """
        return EnrollmentEntity(
            id=model.id,
            user_id=model.user_id,
            course_id=model.course_id,
            is_mandatory=model.is_mandatory,
            status=model.status,
            access_type=model.access_type,
            enrolled_at=model.enrolled_at,
            completed_at=model.completed_at,
            start_date=model.start_date,
            end_date=model.end_date,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: EnrollmentEntity) -> EnrollmentModel:
        """Map an EnrollmentEntity to an EnrollmentModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            EnrollmentModel: The ORM model ready for persistence.
        """
        return EnrollmentModel(
            id=entity.id,
            user_id=entity.user_id,
            course_id=entity.course_id,
            is_mandatory=entity.is_mandatory,
            status=entity.status,
            access_type=entity.access_type,
            enrolled_at=entity.enrolled_at,
            completed_at=entity.completed_at,
            start_date=entity.start_date,
            end_date=entity.end_date,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
