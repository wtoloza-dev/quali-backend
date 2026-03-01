"""Assessment question repository."""

from datetime import UTC, datetime

from pydantic import TypeAdapter
from sqlmodel import asc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.models.entity_tombstone_model import EntityTombstoneModel

from ...domain.entities import QuestionEntity
from ...domain.entities.question_config import MultipleChoiceConfig, QuestionConfig
from ...domain.enums import QuestionType
from ..models.question_model import QuestionModel


_config_adapter = TypeAdapter(QuestionConfig)


class QuestionRepository:
    """Handles all database operations for assessment question entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: QuestionEntity) -> QuestionEntity:
        """Persist a new question entity."""
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, question_id: str) -> QuestionEntity | None:
        """Retrieve a question by its ULID."""
        statement = select(QuestionModel).where(QuestionModel.id == question_id)
        result = await self._session.exec(statement)
        model = result.first()
        return self._to_entity(model) if model else None

    async def list_by_course(self, course_id: str) -> list[QuestionEntity]:
        """List all questions for a course, ordered by position."""
        statement = (
            select(QuestionModel)
            .where(QuestionModel.course_id == course_id)
            .order_by(asc(QuestionModel.order))
        )
        result = await self._session.exec(statement)
        return [self._to_entity(m) for m in result.all()]

    async def list_by_module(self, module_id: str) -> list[QuestionEntity]:
        """List all questions for a module, ordered by position."""
        statement = (
            select(QuestionModel)
            .where(QuestionModel.module_id == module_id)
            .order_by(asc(QuestionModel.order))
        )
        result = await self._session.exec(statement)
        return [self._to_entity(m) for m in result.all()]

    async def delete(self, question_id: str, deleted_by: str) -> None:
        """Soft-delete a question by moving it to the tombstone table."""
        statement = select(QuestionModel).where(QuestionModel.id == question_id)
        result = await self._session.exec(statement)
        model = result.first()
        if model is None:
            return
        tombstone = EntityTombstoneModel(
            entity_type="question",
            entity_id=model.id,
            payload={
                "id": model.id,
                "course_id": model.course_id,
                "text": model.text,
                "question_type": model.question_type,
                "config": model.config,
                "order": model.order,
                "created_at": (
                    model.created_at.isoformat() if model.created_at else None
                ),
                "created_by": model.created_by,
                "updated_at": (
                    model.updated_at.isoformat() if model.updated_at else None
                ),
                "updated_by": model.updated_by,
            },
            deleted_at=datetime.now(UTC),
            deleted_by=deleted_by,
        )
        self._session.add(tombstone)
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _parse_config(raw: dict | None) -> QuestionConfig:
        if not raw or not raw.get("type"):
            return MultipleChoiceConfig()
        return _config_adapter.validate_python(raw)

    @classmethod
    def _to_entity(cls, model: QuestionModel) -> QuestionEntity:
        return QuestionEntity(
            id=model.id,
            course_id=model.course_id,
            module_id=model.module_id,
            text=model.text,
            question_type=QuestionType(model.question_type),
            config=cls._parse_config(model.config),
            randomize=model.randomize if model.randomize is not None else True,
            order=model.order,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )

    @staticmethod
    def _to_model(entity: QuestionEntity) -> QuestionModel:
        return QuestionModel(
            id=entity.id,
            course_id=entity.course_id,
            module_id=entity.module_id,
            text=entity.text,
            question_type=entity.question_type,
            config=entity.config.model_dump(),
            randomize=entity.randomize,
            order=entity.order,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by,
        )
