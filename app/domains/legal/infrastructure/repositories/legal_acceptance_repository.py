"""Legal acceptance repository."""

from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.legal_acceptance_model import LegalAcceptanceModel


class LegalAcceptanceRepository:
    """Write-only repository for legal acceptance records."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, model: LegalAcceptanceModel) -> LegalAcceptanceModel:
        """Persist a legal acceptance record."""
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model
