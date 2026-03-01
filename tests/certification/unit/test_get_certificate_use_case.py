"""Unit tests for GetCertificateUseCase."""

from datetime import UTC, datetime

import pytest

from app.domains.certification.application.use_cases import GetCertificateUseCase
from app.domains.certification.domain.entities import CertificateEntity
from app.domains.certification.domain.exceptions import CertificateNotFoundException


COMPANY_A = "01ARZ3NDEKTSV4RRFFQ69G5FAA"
COMPANY_B = "01ARZ3NDEKTSV4RRFFQ69G5FAB"
CERT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"


def _make_cert(company_id: str = COMPANY_A) -> CertificateEntity:
    now = datetime.now(UTC)
    return CertificateEntity(
        id=CERT_ID,
        company_id=company_id,
        recipient_id="01ARZ3NDEKTSV4RRFFQ69G5FAR",
        title="Test Cert",
        token="01ARZ3NDEKTSV4RRFFQ69G5FAT",
        issued_at=now,
        created_at=now,
        created_by="01ARZ3NDEKTSV4RRFFQ69G5FAU",
        updated_at=now,
        updated_by=None,
    )


class FakeCertificateRepository:
    def __init__(self, cert: CertificateEntity | None = None):
        self._store: dict[str, CertificateEntity] = {cert.id: cert} if cert else {}

    async def save(self, entity): return entity
    async def get_by_id(self, certificate_id): return self._store.get(certificate_id)
    async def get_by_id_and_company(self, certificate_id, company_id):
        entity = self._store.get(certificate_id)
        return entity if entity and entity.company_id == company_id else None
    async def get_by_token(self, token): return None
    async def update(self, entity): return entity
    async def list(self, company_id, page, page_size): return [], 0


class TestGetCertificateUseCase:
    async def test_returns_certificate_when_found(self):
        cert = _make_cert(COMPANY_A)
        use_case = GetCertificateUseCase(repository=FakeCertificateRepository(cert))

        result = await use_case.execute(certificate_id=CERT_ID, company_id=COMPANY_A)

        assert result.id == CERT_ID

    async def test_raises_not_found_for_unknown_id(self):
        use_case = GetCertificateUseCase(repository=FakeCertificateRepository())

        with pytest.raises(CertificateNotFoundException):
            await use_case.execute(certificate_id="unknown", company_id=COMPANY_A)

    async def test_raises_not_found_for_wrong_company(self):
        cert = _make_cert(COMPANY_A)
        use_case = GetCertificateUseCase(repository=FakeCertificateRepository(cert))

        with pytest.raises(CertificateNotFoundException):
            await use_case.execute(certificate_id=CERT_ID, company_id=COMPANY_B)
