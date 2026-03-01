"""Module repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.module_repository import ModuleRepository


def build_module_repository(session: PostgresSessionDependency) -> ModuleRepository:
    """Build a ModuleRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        ModuleRepository: Repository instance ready for use.
    """
    return ModuleRepository(session=session)


ModuleRepositoryDependency = Annotated[
    ModuleRepository,
    Depends(build_module_repository),
]
