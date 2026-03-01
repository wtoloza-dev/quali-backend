"""List questions use case."""

from app.domains.education.courses.domain.exceptions import (
    CourseNotFoundException,
)
from app.domains.education.courses.domain.ports import CourseRepositoryPort

from ...domain.entities import QuestionEntity
from ...domain.ports import QuestionRepositoryPort


class ListQuestionsUseCase:
    """Return all questions in a course's question bank.

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
        course_id: str,
        company_id: str,
    ) -> list[QuestionEntity]:
        """Return all questions for a course after verifying ownership.

        Args:
            course_id: ULID of the course whose questions to list.
            company_id: ULID of the owning company.

        Returns:
            List of QuestionEntity sorted by order.

        Raises:
            CourseNotFoundException: If the course does not exist
                or is not owned by the company.
        """
        course = await self._course_repository.get_by_id_and_company(
            course_id=course_id,
            company_id=company_id,
        )
        if course is None:
            raise CourseNotFoundException(course_id=course_id)

        return await self._repository.list_by_course(course_id=course_id)
