"""Unit tests for AddCompanyMemberUseCase."""

import pytest

from app.domains.companies.application.use_cases import AddCompanyMemberUseCase
from app.domains.companies.domain.entities import CompanyMemberData, CompanyMemberEntity
from app.domains.companies.domain.exceptions import CompanyMemberAlreadyExistsException


COMPANY_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"
USER_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAU"
CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAA"


class FakeCompanyMemberRepository:
    def __init__(self):
        self._store: dict[str, CompanyMemberEntity] = {}

    async def save(self, entity: CompanyMemberEntity) -> CompanyMemberEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_company_and_user(self, company_id, user_id):
        return next(
            (
                e for e in self._store.values()
                if e.company_id == company_id and e.user_id == user_id
            ),
            None,
        )

    async def get_by_company_id(self, company_id): return []
    async def delete(self, company_member_id, deleted_by): self._store.pop(company_member_id, None)


class TestAddCompanyMemberUseCase:
    async def test_adds_member_successfully(self):
        repo = FakeCompanyMemberRepository()
        use_case = AddCompanyMemberUseCase(repository=repo)
        data = CompanyMemberData(company_id=COMPANY_ID, user_id=USER_ID)

        result = await use_case.execute(data=data, created_by=CREATED_BY)

        assert result.company_id == COMPANY_ID
        assert result.user_id == USER_ID
        assert result.created_by == CREATED_BY

    async def test_raises_when_member_already_exists(self):
        repo = FakeCompanyMemberRepository()
        use_case = AddCompanyMemberUseCase(repository=repo)
        data = CompanyMemberData(company_id=COMPANY_ID, user_id=USER_ID)
        await use_case.execute(data=data, created_by=CREATED_BY)

        with pytest.raises(CompanyMemberAlreadyExistsException):
            await use_case.execute(data=data, created_by=CREATED_BY)

    async def test_same_user_can_join_different_companies(self):
        repo = FakeCompanyMemberRepository()
        use_case = AddCompanyMemberUseCase(repository=repo)

        await use_case.execute(
            data=CompanyMemberData(company_id="company-a", user_id=USER_ID),
            created_by=CREATED_BY,
        )
        result = await use_case.execute(
            data=CompanyMemberData(company_id="company-b", user_id=USER_ID),
            created_by=CREATED_BY,
        )

        assert result.company_id == "company-b"
