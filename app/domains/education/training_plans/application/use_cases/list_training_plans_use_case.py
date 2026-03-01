"""List training plans use case."""

from app.shared.schemas.pagination_schema import PaginationParams

from ...domain.entities import TrainingPlanEntity
from ...domain.ports import TrainingPlanRepositoryPort


class ListTrainingPlansUseCase:
    """Return a paginated list of training plans for a company."""

    def __init__(self, repository: TrainingPlanRepositoryPort) -> None:
        """Initialise with the training plan repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        company_id: str,
        params: PaginationParams,
    ) -> tuple[list[TrainingPlanEntity], int]:
        """Return paginated training plans for the given company.

        Args:
            company_id: ULID of the company to scope the listing.
            params: Pagination parameters.

        Returns:
            Tuple of (page of TrainingPlanEntity, total count).
        """
        return await self._repository.list_by_company(
            company_id=company_id,
            page=params.page,
            page_size=params.page_size,
        )
