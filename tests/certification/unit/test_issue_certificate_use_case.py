"""Unit tests for IssueCertificateUseCase."""

from datetime import UTC, datetime

import pytest

from app.domains.certification.application.use_cases import IssueCertificateUseCase
from app.domains.certification.domain.entities import CertificateData, CertificateEntity


COMPANY_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"
RECIPIENT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAR"
CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAU"


class FakeCertificateRepository:
    def __init__(self):
        self._store: dict[str, CertificateEntity] = {}

    async def save(self, entity: CertificateEntity) -> CertificateEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, certificate_id: str) -> CertificateEntity | None:
        return self._store.get(certificate_id)

    async def get_by_id_and_company(self, certificate_id: str, company_id: str) -> CertificateEntity | None:
        entity = self._store.get(certificate_id)
        if entity and entity.company_id == company_id:
            return entity
        return None

    async def get_by_token(self, token: str) -> CertificateEntity | None:
        return next((e for e in self._store.values() if e.token == token), None)

    async def update(self, entity: CertificateEntity) -> CertificateEntity:
        self._store[entity.id] = entity
        return entity

    async def list(self, company_id: str, page: int, page_size: int) -> tuple[list[CertificateEntity], int]:
        items = [e for e in self._store.values() if e.company_id == company_id]
        return items, len(items)


@pytest.fixture
def repo():
    return FakeCertificateRepository()


@pytest.fixture
def use_case(repo):
    return IssueCertificateUseCase(repository=repo)


@pytest.fixture
def valid_data():
    return CertificateData(
        company_id=COMPANY_ID,
        recipient_id=RECIPIENT_ID,
        title="Python Fundamentals",
        description="Completed the course",
    )


class TestIssueCertificateUseCase:
    async def test_returns_persisted_entity(self, use_case, valid_data):
        result = await use_case.execute(data=valid_data, created_by=CREATED_BY)

        assert result.id is not None
        assert result.company_id == COMPANY_ID
        assert result.recipient_id == RECIPIENT_ID
        assert result.title == "Python Fundamentals"

    async def test_generates_unique_token(self, use_case, valid_data):
        a = await use_case.execute(data=valid_data, created_by=CREATED_BY)
        b = await use_case.execute(
            data=CertificateData(company_id=COMPANY_ID, recipient_id=RECIPIENT_ID, title="Other"),
            created_by=CREATED_BY,
        )

        assert a.token != b.token

    async def test_issued_at_defaults_to_now_when_not_provided(self, use_case, valid_data):
        before = datetime.now(UTC)
        result = await use_case.execute(data=valid_data, created_by=CREATED_BY)

        assert result.issued_at is not None
        assert result.issued_at >= before

    async def test_uses_explicit_issued_at_when_provided(self, use_case):
        custom_date = datetime(2025, 1, 1, tzinfo=UTC)
        data = CertificateData(
            company_id=COMPANY_ID,
            recipient_id=RECIPIENT_ID,
            title="Old Course",
            issued_at=custom_date,
        )

        result = await use_case.execute(data=data, created_by=CREATED_BY)

        assert result.issued_at == custom_date

    async def test_certificate_is_active_after_issuance(self, use_case, valid_data):
        from app.domains.certification.domain.enums import CertificateStatus

        result = await use_case.execute(data=valid_data, created_by=CREATED_BY)

        assert result.status == CertificateStatus.ACTIVE
        assert result.is_revokable is True

    async def test_sets_created_by(self, use_case, valid_data):
        result = await use_case.execute(data=valid_data, created_by=CREATED_BY)

        assert result.created_by == CREATED_BY
