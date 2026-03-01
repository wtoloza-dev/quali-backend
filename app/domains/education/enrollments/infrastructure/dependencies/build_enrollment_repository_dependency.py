"""Enrollment repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.enrollment_repository import EnrollmentRepository


def build_enrollment_repository(
    session: PostgresSessionDependency,
) -> EnrollmentRepository:
    """Build an EnrollmentRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        EnrollmentRepository: Repository instance ready for use.
    """
    return EnrollmentRepository(session=session)


EnrollmentRepositoryDependency = Annotated[
    EnrollmentRepository,
    Depends(build_enrollment_repository),
]
