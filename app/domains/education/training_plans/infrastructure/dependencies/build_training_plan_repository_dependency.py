"""Training plan repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.training_plan_repository import TrainingPlanRepository


def build_training_plan_repository(
    session: PostgresSessionDependency,
) -> TrainingPlanRepository:
    """Build a TrainingPlanRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        TrainingPlanRepository: Repository instance ready for use.
    """
    return TrainingPlanRepository(session=session)


TrainingPlanRepositoryDependency = Annotated[
    TrainingPlanRepository,
    Depends(build_training_plan_repository),
]
