"""get_company_member contract adapter.

Concrete implementation of GetCompanyMemberPort. Allowed to import from the
companies domain infrastructure — this is the only place that crosses the
domain boundary for this contract.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.companies.infrastructure.repositories.company_member_repository import (
    CompanyMemberRepository,
)
from app.shared.dependencies.clients.sql.postgres_session_dependency import (
    PostgresSessionDependency,
)

from .get_company_member_port import CompanyMemberContractResult


class GetCompanyMemberAdapter:
    """Fetches a company member and maps to the contract result.

    Wraps CompanyMemberRepository internally so that no caller needs to
    import from the companies domain.

    Attributes:
        _repository: The companies domain repository used for the lookup.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the adapter with a database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._repository = CompanyMemberRepository(session=session)

    async def __call__(
        self, company_id: str, user_id: str
    ) -> CompanyMemberContractResult | None:
        """Retrieve a company member by company and user IDs.

        Args:
            company_id: ULID of the company.
            user_id: ULID of the user.

        Returns:
            CompanyMemberContractResult if found, None otherwise.
        """
        entity = await self._repository.get_by_company_and_user(
            company_id=company_id, user_id=user_id
        )
        if entity is None:
            return None
        return CompanyMemberContractResult(
            company_id=entity.company_id,
            user_id=entity.user_id,
            role=entity.role.value if hasattr(entity.role, "value") else str(entity.role),
        )


def build_get_company_member_adapter(
    session: PostgresSessionDependency,
) -> GetCompanyMemberAdapter:
    """Construct a GetCompanyMemberAdapter with an injected session.

    Args:
        session: Async database session provided by FastAPI.

    Returns:
        GetCompanyMemberAdapter: Ready-to-use adapter instance.
    """
    return GetCompanyMemberAdapter(session=session)


GetCompanyMemberDependency = Annotated[
    GetCompanyMemberAdapter,
    Depends(build_get_company_member_adapter),
]
