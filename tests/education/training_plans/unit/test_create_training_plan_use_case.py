"""Unit tests for CreateTrainingPlanUseCase."""

from app.domains.education.training_plans.application.use_cases import (
    CreateTrainingPlanUseCase,
)
from app.domains.education.training_plans.domain.entities import (
    TrainingPlanData,
    TrainingPlanEntity,
)
from app.domains.education.training_plans.domain.enums import TrainingPlanStatus


COMPANY_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"
CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAA"


class FakeTrainingPlanRepository:
    def __init__(self) -> None:
        self._store: dict[str, TrainingPlanEntity] = {}

    async def save(self, entity: TrainingPlanEntity) -> TrainingPlanEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, plan_id):
        return self._store.get(plan_id)

    async def get_by_id_and_company(self, plan_id: str, company_id: str):
        entity = self._store.get(plan_id)
        if entity is None or entity.company_id != company_id:
            return None
        return entity


    async def update(self, entity):
        self._store[entity.id] = entity
        return entity

    async def delete(self, plan_id, deleted_by):
        self._store.pop(plan_id, None)

    async def list_by_company(self, company_id, page, page_size):
        items = [e for e in self._store.values() if e.company_id == company_id]
        offset = (page - 1) * page_size
        return items[offset : offset + page_size], len(items)


class TestCreateTrainingPlanUseCase:
    async def test_creates_plan_successfully(self):
        repo = FakeTrainingPlanRepository()
        use_case = CreateTrainingPlanUseCase(repository=repo)
        data = TrainingPlanData(company_id=COMPANY_ID, year=2026, title="Annual Plan")

        result = await use_case.execute(data=data, created_by=CREATED_BY)

        assert result.id is not None
        assert result.company_id == COMPANY_ID
        assert result.year == 2026
        assert result.title == "Annual Plan"
        assert result.created_by == CREATED_BY

    async def test_initial_status_is_draft(self):
        repo = FakeTrainingPlanRepository()
        use_case = CreateTrainingPlanUseCase(repository=repo)
        data = TrainingPlanData(company_id=COMPANY_ID, year=2026, title="Plan")

        result = await use_case.execute(data=data, created_by=CREATED_BY)

        assert result.status == TrainingPlanStatus.DRAFT

    async def test_generates_unique_ids(self):
        repo = FakeTrainingPlanRepository()
        use_case = CreateTrainingPlanUseCase(repository=repo)

        r1 = await use_case.execute(
            data=TrainingPlanData(company_id=COMPANY_ID, year=2026, title="Plan A"),
            created_by=CREATED_BY,
        )
        r2 = await use_case.execute(
            data=TrainingPlanData(company_id=COMPANY_ID, year=2027, title="Plan B"),
            created_by=CREATED_BY,
        )

        assert r1.id != r2.id
