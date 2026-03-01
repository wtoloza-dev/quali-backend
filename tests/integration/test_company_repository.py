"""Integration tests for CompanyRepository against a real PostgreSQL container."""

import pytest

from app.domains.companies.domain.entities import CompanyEntity
from app.domains.companies.domain.enums import CompanyType, Country
from app.domains.companies.infrastructure.repositories.company_repository import (
    CompanyRepository,
)


pytestmark = pytest.mark.integration

COMPANY_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"
CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAA"


def _make_entity(company_id: str = COMPANY_ID, slug: str = "acme-corp") -> CompanyEntity:
    from datetime import UTC, datetime
    now = datetime.now(UTC)
    return CompanyEntity(
        id=company_id,
        name="Acme Corp",
        slug=slug,
        company_type=CompanyType.ORGANIZATION,
        email="contact@acme.com",
        country=Country.CO,
        tax=None,
        legal_name=None,
        logo_url=None,
        created_at=now,
        created_by=CREATED_BY,
        updated_at=now,
        updated_by=None,
    )


class TestCompanyRepository:
    async def test_save_and_get_by_id(self, session):
        repo = CompanyRepository(session=session)
        entity = _make_entity()

        saved = await repo.save(entity)
        found = await repo.get_by_id(COMPANY_ID)

        assert found is not None
        assert found.id == saved.id
        assert found.slug == "acme-corp"

    async def test_get_by_id_returns_none_for_unknown(self, session):
        repo = CompanyRepository(session=session)

        result = await repo.get_by_id("nonexistent-id")

        assert result is None

    async def test_get_by_slug(self, session):
        repo = CompanyRepository(session=session)
        await repo.save(_make_entity())

        found = await repo.get_by_slug("acme-corp")

        assert found is not None
        assert found.id == COMPANY_ID

    async def test_get_by_slug_returns_none_for_unknown(self, session):
        repo = CompanyRepository(session=session)

        result = await repo.get_by_slug("does-not-exist")

        assert result is None

    async def test_get_by_id_excludes_soft_deleted(self, session):
        repo = CompanyRepository(session=session)
        await repo.save(_make_entity())
        await repo.delete(COMPANY_ID, deleted_by=CREATED_BY)

        found = await repo.get_by_id(COMPANY_ID)

        assert found is None

    async def test_get_by_slug_excludes_soft_deleted(self, session):
        repo = CompanyRepository(session=session)
        await repo.save(_make_entity())
        await repo.delete(COMPANY_ID, deleted_by=CREATED_BY)

        found = await repo.get_by_slug("acme-corp")

        assert found is None

    async def test_unique_constraint_on_slug(self, session):
        from sqlalchemy.exc import IntegrityError
        repo = CompanyRepository(session=session)
        await repo.save(_make_entity())

        with pytest.raises((IntegrityError, Exception)):
            await repo.save(_make_entity(company_id="01ARZ3NDEKTSV4RRFFQ69G5FAX"))
