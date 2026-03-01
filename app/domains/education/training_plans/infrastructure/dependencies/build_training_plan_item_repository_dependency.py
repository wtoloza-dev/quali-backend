"""Training plan item repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.training_plan_item_repository import TrainingPlanItemRepository


def build_training_plan_item_repository(
    session: PostgresSessionDependency,
) -> TrainingPlanItemRepository:
    """Build a TrainingPlanItemRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        TrainingPlanItemRepository: Repository instance ready for use.
    """
    return TrainingPlanItemRepository(session=session)


TrainingPlanItemRepositoryDependency = Annotated[
    TrainingPlanItemRepository,
    Depends(build_training_plan_item_repository),
]
