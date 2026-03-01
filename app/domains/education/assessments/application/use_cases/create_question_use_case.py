"""Create assessment question use case."""

from datetime import UTC, datetime

from ulid import ULID

from app.domains.education.courses.domain.exceptions import (
    CourseNotFoundException,
)
from app.domains.education.courses.domain.ports import CourseRepositoryPort

from ...domain.entities import QuestionData, QuestionEntity
from ...domain.ports import QuestionRepositoryPort


class CreateQuestionUseCase:
    """Add a new question to a course's question bank.

    Args:
        course_repository: Port to verify course ownership.
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(
        self,
        course_repository: CourseRepositoryPort,
        repository: QuestionRepositoryPort,
    ) -> None:
        """Initialise with required repositories.

        Args:
            course_repository: Injected course repository.
            repository: Concrete question repository injected by
                the infrastructure layer.
        """
        self._course_repository = course_repository
        self._repository = repository

    async def execute(
        self,
        data: QuestionData,
        company_id: str,
        created_by: str,
    ) -> QuestionEntity:
        """Persist a new question after verifying tenant ownership.

        Args:
            data: Question data including text, type, and options.
            company_id: ULID of the owning company.
            created_by: ULID of the actor creating the question.

        Returns:
            QuestionEntity: The persisted question.

        Raises:
            CourseNotFoundException: If the course does not exist
                or is not owned by the company.
        """
        course = await self._course_repository.get_by_id_and_company(
            course_id=data.course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=data.course_id)

        now = datetime.now(UTC)
        entity = QuestionEntity(
            id=str(ULID()),
            course_id=data.course_id,
            module_id=data.module_id,
            text=data.text,
            question_type=data.question_type,
            config=data.config,
            randomize=data.randomize,
            order=data.order,
            created_at=now,
            created_by=created_by,
            updated_at=None,
            updated_by=None,
        )
        return await self._repository.save(entity)
