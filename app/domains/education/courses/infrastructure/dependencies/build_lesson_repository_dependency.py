"""Lesson repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.lesson_repository import LessonRepository


def build_lesson_repository(session: PostgresSessionDependency) -> LessonRepository:
    """Build a LessonRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        LessonRepository: Repository instance ready for use.
    """
    return LessonRepository(session=session)


LessonRepositoryDependency = Annotated[
    LessonRepository,
    Depends(build_lesson_repository),
]
