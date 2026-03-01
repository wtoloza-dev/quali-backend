"""Unit tests for VerifyCertificateUseCase."""

from datetime import UTC, datetime

import pytest

from app.domains.certification.application.use_cases import VerifyCertificateUseCase
from app.domains.certification.domain.entities import CertificateEntity
from app.domains.certification.domain.exceptions import CertificateNotFoundException


TOKEN = "01ARZ3NDEKTSV4RRFFQ69G5FAT"
CERT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"


def _make_cert() -> CertificateEntity:
    now = datetime.now(UTC)
    return CertificateEntity(
        id=CERT_ID,
        company_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        recipient_id="01ARZ3NDEKTSV4RRFFQ69G5FAR",
        title="Test Cert",
        token=TOKEN,
        issued_at=now,
        created_at=now,
        created_by="01ARZ3NDEKTSV4RRFFQ69G5FAU",
        updated_at=now,
        updated_by=None,
    )


class FakeCertificateRepository:
    def __init__(self, cert: CertificateEntity | None = None):
        self._by_token: dict[str, CertificateEntity] = (
            {cert.token: cert} if cert else {}
        )

    async def save(self, entity): return entity
    async def get_by_id(self, certificate_id): return None
    async def get_by_id_and_company(self, certificate_id, company_id): return None
    async def get_by_token(self, token): return self._by_token.get(token)
    async def update(self, entity): return entity
    async def list(self, company_id, page, page_size): return [], 0


class TestVerifyCertificateUseCase:
    async def test_returns_certificate_for_valid_token(self):
        cert = _make_cert()
        use_case = VerifyCertificateUseCase(repository=FakeCertificateRepository(cert))

        result = await use_case.execute(token=TOKEN)

        assert result.id == CERT_ID
        assert result.token == TOKEN

    async def test_raises_not_found_for_unknown_token(self):
        use_case = VerifyCertificateUseCase(repository=FakeCertificateRepository())

        with pytest.raises(CertificateNotFoundException):
            await use_case.execute(token="unknown-token")
