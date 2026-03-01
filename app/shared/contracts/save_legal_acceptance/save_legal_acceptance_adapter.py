"""save_legal_acceptance contract adapter.

Concrete implementation of SaveLegalAcceptancePort. Allowed to import from
the legal domain infrastructure — this is the only place that crosses the
domain boundary for this contract.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.legal.infrastructure.models.legal_acceptance_model import (
    LegalAcceptanceModel,
)
from app.domains.legal.infrastructure.repositories.legal_acceptance_repository import (
    LegalAcceptanceRepository,
)
from app.shared.dependencies.clients.sql.postgres_session_dependency import (
    PostgresSessionDependency,
)

from .save_legal_acceptance_port import LegalAcceptanceContractInput


class SaveLegalAcceptanceAdapter:
    """Saves a legal acceptance record via the legal domain repository.

    Wraps LegalAcceptanceRepository internally so that no caller needs to
    import from the legal domain.

    Attributes:
        _repository: The legal domain repository used for persistence.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the adapter with a database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._repository = LegalAcceptanceRepository(session=session)

    async def __call__(self, data: LegalAcceptanceContractInput) -> None:
        """Save a legal acceptance record.

        Args:
            data: The acceptance data to persist.
        """
        model = LegalAcceptanceModel(
            user_id=data.user_id,
            enrollment_id=data.enrollment_id,
            acceptance_type=data.acceptance_type,
            declaration_text=data.declaration_text,
            ip_address=data.ip_address,
        )
        await self._repository.save(model)


def build_save_legal_acceptance_adapter(
    session: PostgresSessionDependency,
) -> SaveLegalAcceptanceAdapter:
    """Construct a SaveLegalAcceptanceAdapter with an injected session.

    Args:
        session: Async database session provided by FastAPI.

    Returns:
        SaveLegalAcceptanceAdapter: Ready-to-use adapter instance.
    """
    return SaveLegalAcceptanceAdapter(session=session)


SaveLegalAcceptanceDependency = Annotated[
    SaveLegalAcceptanceAdapter,
    Depends(build_save_legal_acceptance_adapter),
]
