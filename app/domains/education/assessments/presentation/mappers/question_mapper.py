"""Question entity-to-schema mapper."""

from ...domain.entities import QuestionEntity
from ..schemas.question_response_schema import QuestionResponseSchema


class QuestionMapper:
    """Converts between QuestionEntity and question response schemas."""

    @staticmethod
    def to_response(entity: QuestionEntity) -> QuestionResponseSchema:
        """Map a QuestionEntity to its API response schema."""
        return QuestionResponseSchema(
            id=entity.id,
            course_id=entity.course_id,
            module_id=entity.module_id,
            text=entity.text,
            question_type=entity.question_type,
            config=entity.config,
            randomize=entity.randomize,
            order=entity.order,
            created_at=entity.created_at,
            created_by=entity.created_by,
        )
