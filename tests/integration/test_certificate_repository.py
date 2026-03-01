"""Integration tests for CertificateRepository against a real PostgreSQL container."""

import pytest

from app.domains.certification.domain.entities import CertificateEntity
from app.domains.certification.infrastructure.repositories.certificate_repository import (
    CertificateRepository,
)


pytestmark = pytest.mark.integration

COMPANY_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"
OTHER_COMPANY_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAX"
CERT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAT"
RECIPIENT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAR"
CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAA"
TOKEN = "01ARZ3NDEKTSV4RRFFQ69G5FAK"


def _make_entity(
    cert_id: str = CERT_ID,
    company_id: str = COMPANY_ID,
    token: str = TOKEN,
) -> CertificateEntity:
    from datetime import UTC, datetime
    now = datetime.now(UTC)
    return CertificateEntity(
        id=cert_id,
        company_id=company_id,
        recipient_id=RECIPIENT_ID,
        title="Python Fundamentals",
        description=None,
        token=token,
        issued_at=now,
        expires_at=None,
        created_at=now,
        created_by=CREATED_BY,
        updated_at=now,
        updated_by=None,
    )


class TestCertificateRepository:
    async def test_save_and_get_by_id(self, session):
        repo = CertificateRepository(session=session)
        entity = _make_entity()

        saved = await repo.save(entity)
        found = await repo.get_by_id(CERT_ID)

        assert found is not None
        assert found.id == saved.id
        assert found.title == "Python Fundamentals"

    async def test_get_by_id_returns_none_for_unknown(self, session):
        repo = CertificateRepository(session=session)

        result = await repo.get_by_id("nonexistent-id")

        assert result is None

    async def test_get_by_token(self, session):
        repo = CertificateRepository(session=session)
        await repo.save(_make_entity())

        found = await repo.get_by_token(TOKEN)

        assert found is not None
        assert found.id == CERT_ID

    async def test_get_by_id_and_company_returns_entity(self, session):
        repo = CertificateRepository(session=session)
        await repo.save(_make_entity())

        found = await repo.get_by_id_and_company(CERT_ID, COMPANY_ID)

        assert found is not None
        assert found.id == CERT_ID

    async def test_get_by_id_and_company_returns_none_for_wrong_company(self, session):
        repo = CertificateRepository(session=session)
        await repo.save(_make_entity())

        found = await repo.get_by_id_and_company(CERT_ID, OTHER_COMPANY_ID)

        assert found is None

    async def test_list_returns_only_company_certificates(self, session):
        repo = CertificateRepository(session=session)
        await repo.save(_make_entity(cert_id=CERT_ID, company_id=COMPANY_ID, token=TOKEN))
        await repo.save(_make_entity(
            cert_id="01ARZ3NDEKTSV4RRFFQ69G5FAY",
            company_id=OTHER_COMPANY_ID,
            token="01ARZ3NDEKTSV4RRFFQ69G5FAZ",
        ))

        items, total = await repo.list(company_id=COMPANY_ID, page=1, page_size=10)

        assert total == 1
        assert items[0].id == CERT_ID

    async def test_list_pagination(self, session):
        repo = CertificateRepository(session=session)
        tokens = [f"0{i}ARZ3NDEKTSV4RRFFQ69G5FAK" for i in range(3)]
        ids = [f"0{i}ARZ3NDEKTSV4RRFFQ69G5FAT" for i in range(3)]
        for cert_id, token in zip(ids, tokens):
            await repo.save(_make_entity(cert_id=cert_id, token=token))

        items, total = await repo.list(company_id=COMPANY_ID, page=1, page_size=2)

        assert total == 3
        assert len(items) == 2

    async def test_revoke_persists_via_update(self, session):
        from datetime import UTC, datetime
        repo = CertificateRepository(session=session)
        entity = await repo.save(_make_entity())

        revoked = entity.model_copy(update={
            "revoked_at": datetime.now(UTC),
            "revoked_by": CREATED_BY,
            "revoked_reason": "Test revocation.",
        })
        await repo.update(revoked)

        found = await repo.get_by_id(CERT_ID)
        assert found.revoked_at is not None
        assert found.status.value == "revoked"
