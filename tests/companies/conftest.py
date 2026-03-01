"""Shared fixtures for the companies domain tests."""

from datetime import UTC, datetime

import pytest

from app.domains.companies.domain.entities import CompanyEntity
from app.domains.companies.domain.enums import CompanyType, Country, TaxType
from app.domains.companies.domain.ports import CompanyRepositoryPort
from app.domains.companies.domain.value_objects import Tax


class FakeCompanyRepository:
    """In-memory implementation of CompanyRepositoryPort for testing.

    Stores entities in a dict keyed by ULID. Used via dependency
    override — never patches source code.
    """

    def __init__(self) -> None:
        self._store: dict[str, CompanyEntity] = {}

    async def save(self, entity: CompanyEntity) -> CompanyEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, company_id: str) -> CompanyEntity | None:
        return self._store.get(company_id)

    async def get_by_slug(self, slug: str) -> CompanyEntity | None:
        return next(
            (e for e in self._store.values() if e.slug == slug),
            None,
        )

    async def update(self, entity: CompanyEntity) -> CompanyEntity:
        self._store[entity.id] = entity
        return entity

    async def delete(self, company_id: str, deleted_by: str) -> None:
        self._store.pop(company_id, None)


# Verify FakeCompanyRepository satisfies the protocol at import time
_: CompanyRepositoryPort = FakeCompanyRepository()  # type: ignore[assignment]


@pytest.fixture
def fake_company_repository() -> FakeCompanyRepository:
    """Fresh in-memory repository for each test."""
    return FakeCompanyRepository()


@pytest.fixture
def company_entity() -> CompanyEntity:
    """A fully populated CompanyEntity for use in assertions."""
    now = datetime.now(UTC)
    return CompanyEntity(
        id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        name="Acme Corp",
        slug="acme-corp",
        company_type=CompanyType.ORGANIZATION,
        email="contact@acme.com",
        country=Country.CO,
        tax=Tax(tax_type=TaxType.NIT, tax_id="900123456"),
        legal_name="Acme Corporation SAS",
        logo_url=None,
        created_at=now,
        created_by="01ARZ3NDEKTSV4RRFFQ69G5FAB",
        updated_at=now,
        updated_by=None,
    )
