"""Legal acceptance repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.legal_acceptance_repository import LegalAcceptanceRepository


def build_legal_acceptance_repository(
    session: PostgresSessionDependency,
) -> LegalAcceptanceRepository:
    """Build a LegalAcceptanceRepository with an injected async session."""
    return LegalAcceptanceRepository(session=session)


LegalAcceptanceRepositoryDependency = Annotated[
    LegalAcceptanceRepository,
    Depends(build_legal_acceptance_repository),
]
