"""get_company_by_id contract adapter.

Concrete implementation of GetCompanyByIdPort. Allowed to import from the
companies domain infrastructure — this is the only place that crosses the
domain boundary for this contract.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.companies.infrastructure.repositories.company_repository import (
    CompanyRepository,
)
from app.shared.dependencies.clients.sql.postgres_session_dependency import (
    PostgresSessionDependency,
)

from .get_company_by_id_port import CompanyContractResult


class GetCompanyByIdAdapter:
    """Fetches a company by ULID and maps it to CompanyContractResult.

    Wraps CompanyRepository internally so that no caller needs to import
    from the companies domain.

    Attributes:
        _repository: The companies domain repository used for the lookup.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the adapter with a database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._repository = CompanyRepository(session=session)

    async def __call__(self, company_id: str) -> CompanyContractResult | None:
        """Retrieve a company by its ULID.

        Args:
            company_id: ULID of the company to look up.

        Returns:
            CompanyContractResult if the company exists, None otherwise.
        """
        entity = await self._repository.get_by_id(company_id)
        if entity is None:
            return None
        return CompanyContractResult(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            logo_url=entity.logo_url,
        )


def build_get_company_by_id_adapter(
    session: PostgresSessionDependency,
) -> GetCompanyByIdAdapter:
    """Construct a GetCompanyByIdAdapter with an injected session.

    Args:
        session: Async database session provided by FastAPI.

    Returns:
        GetCompanyByIdAdapter: Ready-to-use adapter instance.
    """
    return GetCompanyByIdAdapter(session=session)


GetCompanyByIdDependency = Annotated[
    GetCompanyByIdAdapter,
    Depends(build_get_company_by_id_adapter),
]
