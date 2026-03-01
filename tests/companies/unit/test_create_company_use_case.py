"""Unit tests for CreateCompanyUseCase."""

import pytest

from app.domains.companies.application.use_cases import CreateCompanyUseCase
from app.domains.companies.domain.entities import CompanyData, CompanyEntity
from app.domains.companies.domain.enums import CompanyType, Country, TaxType
from app.domains.companies.domain.exceptions import CompanySlugTakenException
from app.domains.companies.domain.value_objects import Tax


CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAU"


def _valid_data(slug: str = "acme-corp") -> CompanyData:
    return CompanyData(
        name="Acme Corp",
        slug=slug,
        company_type=CompanyType.ORGANIZATION,
        email="contact@acme.com",
        country=Country.CO,
        tax=Tax(tax_type=TaxType.NIT, tax_id="900123456"),
    )


class FakeCompanyRepository:
    def __init__(self):
        self._store: dict[str, CompanyEntity] = {}

    async def save(self, entity: CompanyEntity) -> CompanyEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, company_id): return self._store.get(company_id)
    async def get_by_slug(self, slug):
        return next((e for e in self._store.values() if e.slug == slug), None)
    async def update(self, entity): return entity
    async def delete(self, company_id, deleted_by): self._store.pop(company_id, None)


class TestCreateCompanyUseCase:
    async def test_creates_company_successfully(self):
        repo = FakeCompanyRepository()
        use_case = CreateCompanyUseCase(repository=repo)

        result = await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        assert result.id is not None
        assert result.slug == "acme-corp"
        assert result.created_by == CREATED_BY

    async def test_raises_when_slug_is_taken(self):
        repo = FakeCompanyRepository()
        use_case = CreateCompanyUseCase(repository=repo)
        await use_case.execute(data=_valid_data("taken-slug"), created_by=CREATED_BY)

        with pytest.raises(CompanySlugTakenException):
            await use_case.execute(data=_valid_data("taken-slug"), created_by=CREATED_BY)

    async def test_different_slugs_create_separate_companies(self):
        repo = FakeCompanyRepository()
        use_case = CreateCompanyUseCase(repository=repo)

        a = await use_case.execute(data=_valid_data("slug-a"), created_by=CREATED_BY)
        b = await use_case.execute(data=_valid_data("slug-b"), created_by=CREATED_BY)

        assert a.id != b.id
