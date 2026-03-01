"""Delete assessment question use case."""

from app.domains.education.courses.domain.exceptions import (
    CourseNotFoundException,
)
from app.domains.education.courses.domain.ports import CourseRepositoryPort

from ...domain.exceptions import QuestionNotFoundException
from ...domain.ports import QuestionRepositoryPort


class DeleteQuestionUseCase:
    """Remove a question from a course's question bank.

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
        question_id: str,
        course_id: str,
        company_id: str,
        deleted_by: str,
    ) -> None:
        """Hard-delete a question after verifying tenant ownership.

        Args:
            question_id: ULID of the question to delete.
            course_id: ULID of the parent course.
            company_id: ULID of the owning company.
            deleted_by: ULID of the user performing the deletion.

        Raises:
            CourseNotFoundException: If the course does not exist
                or is not owned by the company.
            QuestionNotFoundException: If no question with that
                ID exists.
        """
        course = await self._course_repository.get_by_id_and_company(
            course_id=course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=course_id)

        entity = await self._repository.get_by_id(question_id)
        if entity is None:
            raise QuestionNotFoundException(question_id)

        await self._repository.delete(
            question_id=question_id,
            deleted_by=deleted_by,
        )
