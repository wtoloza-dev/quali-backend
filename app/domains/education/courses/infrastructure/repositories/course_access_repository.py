"""Course access repository."""

from datetime import UTC, datetime

from sqlmodel import and_, or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ...domain.entities import CourseAccessEntity
from ..models.course_access_model import CourseAccessModel


class CourseAccessRepository:
    """Handles all database operations for course access records.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: CourseAccessEntity) -> CourseAccessEntity:
        """Persist a new course access record.

        Args:
            entity: The course access entity to persist.

        Returns:
            CourseAccessEntity: The persisted entity.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_active_access(
        self, user_id: str, course_id: str
    ) -> CourseAccessEntity | None:
        """Return active (non-expired) access for a user+course pair.

        A row is active when expires_at is NULL (permanent) or in the future.

        Args:
            user_id: The user's ULID.
            course_id: The course's ULID.

        Returns:
            CourseAccessEntity if active access exists, None otherwise.
        """
        now = datetime.now(UTC)
        statement = select(CourseAccessModel).where(
            and_(
                CourseAccessModel.user_id == user_id,
                CourseAccessModel.course_id == course_id,
                or_(
                    CourseAccessModel.expires_at.is_(None),  # type: ignore[union-attr]
                    CourseAccessModel.expires_at > now,
                ),
            )
        )
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: CourseAccessModel) -> CourseAccessEntity:
        """Map a CourseAccessModel to a CourseAccessEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            CourseAccessEntity: The domain entity representation.
        """
        return CourseAccessEntity(
            id=model.id,
            user_id=model.user_id,
            course_id=model.course_id,
            access_type=model.access_type,
            expires_at=model.expires_at,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: CourseAccessEntity) -> CourseAccessModel:
        """Map a CourseAccessEntity to a CourseAccessModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            CourseAccessModel: The ORM model ready for persistence.
        """
        return CourseAccessModel(
            id=entity.id,
            user_id=entity.user_id,
            course_id=entity.course_id,
            access_type=entity.access_type,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
