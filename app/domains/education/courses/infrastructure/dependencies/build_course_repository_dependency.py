"""Course repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.course_repository import CourseRepository


def build_course_repository(session: PostgresSessionDependency) -> CourseRepository:
    """Build a CourseRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        CourseRepository: Repository instance ready for use.
    """
    return CourseRepository(session=session)


CourseRepositoryDependency = Annotated[
    CourseRepository,
    Depends(build_course_repository),
]
