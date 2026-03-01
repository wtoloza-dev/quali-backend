"""Assessment attempt repository."""

from sqlmodel import asc, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ...domain.entities import AnswerEntry, AttemptEntity
from ..models.attempt_model import AttemptModel


class AttemptRepository:
    """Handles all database operations for assessment attempt entities.

    Attributes:
        _session: The async database session for this unit of work.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the repository with an async database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._session = session

    async def save(self, entity: AttemptEntity) -> AttemptEntity:
        """Persist a new attempt and return the saved state.

        Args:
            entity: The attempt entity to persist.

        Returns:
            AttemptEntity: The persisted entity with DB-generated fields.
        """
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def count_by_enrollment(self, enrollment_id: str) -> int:
        """Count the number of attempts for a given enrollment.

        Args:
            enrollment_id: The ULID of the enrollment.

        Returns:
            Number of existing attempts.
        """
        statement = (
            select(func.count())
            .select_from(AttemptModel)
            .where(AttemptModel.enrollment_id == enrollment_id)
        )
        return (await self._session.exec(statement)).one()

    async def count_by_enrollment_and_module(
        self, enrollment_id: str, module_id: str
    ) -> int:
        """Count attempts for a given enrollment and module.

        Args:
            enrollment_id: The ULID of the enrollment.
            module_id: The ULID of the module.

        Returns:
            Number of existing attempts for that module.
        """
        statement = (
            select(func.count())
            .select_from(AttemptModel)
            .where(
                AttemptModel.enrollment_id == enrollment_id,
                AttemptModel.module_id == module_id,
            )
        )
        return (await self._session.exec(statement)).one()

    async def list_by_enrollment(self, enrollment_id: str) -> list[AttemptEntity]:
        """Return all attempts for an enrollment ordered by attempt_number.

        Args:
            enrollment_id: The ULID of the enrollment.

        Returns:
            List of AttemptEntity sorted by attempt_number ascending.
        """
        statement = (
            select(AttemptModel)
            .where(AttemptModel.enrollment_id == enrollment_id)
            .order_by(asc(AttemptModel.attempt_number))
        )
        result = await self._session.exec(statement)
        return [self._to_entity(m) for m in result.all()]

    @staticmethod
    def _to_entity(model: AttemptModel) -> AttemptEntity:
        """Map an AttemptModel ORM instance to an AttemptEntity.

        Args:
            model: The ORM model to convert.

        Returns:
            AttemptEntity: The domain entity representation.
        """
        answers = [
            AnswerEntry(
                question_id=a["question_id"],
                selected_indices=a["selected_indices"],
            )
            for a in (model.answers or [])
        ]
        return AttemptEntity(
            id=model.id,
            enrollment_id=model.enrollment_id,
            module_id=model.module_id,
            score=model.score,
            passed=model.passed,
            attempt_number=model.attempt_number,
            answers=answers,
            correct_question_ids=model.correct_question_ids or [],
            taken_at=model.taken_at,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: AttemptEntity) -> AttemptModel:
        """Map an AttemptEntity to an AttemptModel ORM instance.

        Args:
            entity: The domain entity to convert.

        Returns:
            AttemptModel: The ORM model ready for persistence.
        """
        return AttemptModel(
            id=entity.id,
            enrollment_id=entity.enrollment_id,
            module_id=entity.module_id,
            score=entity.score,
            passed=entity.passed,
            attempt_number=entity.attempt_number,
            answers=[a.model_dump() for a in entity.answers],
            correct_question_ids=entity.correct_question_ids,
            taken_at=entity.taken_at,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
