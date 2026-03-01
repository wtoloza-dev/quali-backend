"""list_certificates_by_recipient contract adapter.

Concrete implementation of ListCertificatesByRecipientPort. Allowed to
import from the certification domain infrastructure — this is the only
place that crosses the domain boundary for this contract.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.certification.infrastructure.repositories.certificate_repository import (
    CertificateRepository,
)
from app.shared.dependencies.clients.sql.postgres_session_dependency import (
    PostgresSessionDependency,
)

from .list_certificates_by_recipient_port import (
    CertificateContractResult,
    CertificateListContractResult,
)


class ListCertificatesByRecipientAdapter:
    """Lists certificates by recipient and maps them to contract DTOs."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the adapter with a database session."""
        self._repository = CertificateRepository(session=session)

    async def __call__(
        self, recipient_id: str, page: int, page_size: int
    ) -> CertificateListContractResult:
        """Retrieve a paginated list of certificates for a recipient."""
        entities, total = await self._repository.list_by_recipient(
            recipient_id=recipient_id, page=page, page_size=page_size
        )
        items = [
            CertificateContractResult(
                id=e.id,
                company_id=e.company_id,
                recipient_id=e.recipient_id,
                title=e.title,
                description=e.description,
                token=e.token,
                status=e.status.value if hasattr(e.status, "value") else str(e.status),
                issued_at=e.issued_at,
                expires_at=e.expires_at,
                revoked_at=e.revoked_at,
            )
            for e in entities
        ]
        page_count = (total + page_size - 1) // page_size if page_size > 0 else 0
        return CertificateListContractResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=page_count,
        )


def build_list_certificates_by_recipient_adapter(
    session: PostgresSessionDependency,
) -> ListCertificatesByRecipientAdapter:
    """Construct adapter with an injected session."""
    return ListCertificatesByRecipientAdapter(session=session)


ListCertificatesByRecipientDependency = Annotated[
    ListCertificatesByRecipientAdapter,
    Depends(build_list_certificates_by_recipient_adapter),
]
