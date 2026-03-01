"""Question repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.question_repository import QuestionRepository


def build_question_repository(
    session: PostgresSessionDependency,
) -> QuestionRepository:
    """Build a QuestionRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        QuestionRepository: Repository instance ready for use.
    """
    return QuestionRepository(session=session)


QuestionRepositoryDependency = Annotated[
    QuestionRepository,
    Depends(build_question_repository),
]
