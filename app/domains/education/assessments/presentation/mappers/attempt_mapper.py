"""Attempt entity-to-schema mapper."""

from ...domain.entities import AttemptEntity
from ..schemas.attempt_response_schema import (
    AnswerEntryResponseSchema,
    AttemptResponseSchema,
)


class AttemptMapper:
    """Converts between AttemptEntity and attempt response schemas."""

    @staticmethod
    def to_response(entity: AttemptEntity) -> AttemptResponseSchema:
        """Map an AttemptEntity to a response schema.

        Args:
            entity: The attempt entity to serialize.

        Returns:
            AttemptResponseSchema: Serialized attempt with score and answers.
        """
        return AttemptResponseSchema(
            id=entity.id,
            enrollment_id=entity.enrollment_id,
            module_id=entity.module_id,
            score=entity.score,
            passed=entity.passed,
            attempt_number=entity.attempt_number,
            answers=[
                AnswerEntryResponseSchema(
                    question_id=a.question_id,
                    selected_indices=a.selected_indices,
                    found_words=a.found_words,
                    cell_answers=a.cell_answers,
                )
                for a in entity.answers
            ],
            correct_question_ids=entity.correct_question_ids,
            taken_at=entity.taken_at,
            created_at=entity.created_at,
        )
