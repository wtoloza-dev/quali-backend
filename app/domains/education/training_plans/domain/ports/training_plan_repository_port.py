"""Training plan repository port."""

from typing import Protocol

from ..entities import TrainingPlanEntity


class TrainingPlanRepositoryPort(Protocol):
    """Interface for the training plan repository."""

    async def save(self, entity: TrainingPlanEntity) -> TrainingPlanEntity:
        """Persist a new training plan and return it."""
        ...

    async def get_by_id(self, plan_id: str) -> TrainingPlanEntity | None:
        """Return a training plan by ID, or None if not found."""
        ...

    async def get_by_id_and_company(
        self, plan_id: str, company_id: str
    ) -> TrainingPlanEntity | None:
        """Retrieve a training plan scoped to a specific company.

        Returns None if the plan does not exist or belongs to a
        different company, preventing cross-tenant data access.

        Args:
            plan_id: The ULID of the training plan.
            company_id: The ULID of the owning company.

        Returns:
            TrainingPlanEntity if found within the company,
            None otherwise.
        """
        ...

    async def update(self, entity: TrainingPlanEntity) -> TrainingPlanEntity:
        """Persist changes to an existing training plan and return it."""
        ...

    async def delete(self, plan_id: str, deleted_by: str) -> None:
        """Hard-delete a training plan after saving a tombstone."""
        ...

    async def list_by_company(
        self,
        company_id: str,
        page: int,
        page_size: int,
    ) -> tuple[list[TrainingPlanEntity], int]:
        """Return a paginated list of training plans for a company."""
        ...
