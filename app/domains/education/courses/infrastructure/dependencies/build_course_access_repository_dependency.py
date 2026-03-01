"""Course access repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.course_access_repository import CourseAccessRepository


def build_course_access_repository(
    session: PostgresSessionDependency,
) -> CourseAccessRepository:
    """Build a CourseAccessRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        CourseAccessRepository: Repository instance ready for use.
    """
    return CourseAccessRepository(session=session)


CourseAccessRepositoryDependency = Annotated[
    CourseAccessRepository,
    Depends(build_course_access_repository),
]
