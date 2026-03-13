"""get_user_by_id contract adapter.

Concrete implementation of GetUserByIdPort. Allowed to import from the
users domain infrastructure — this is the only place that crosses the
domain boundary for this contract.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.users.infrastructure.repositories.user_repository import UserRepository
from app.shared.dependencies.clients.sql.postgres_session_dependency import (
    PostgresSessionDependency,
)

from .get_user_by_id_port import UserContractResult


class GetUserByIdAdapter:
    """Fetches a user by ULID and maps it to UserContractResult.

    Wraps UserRepository internally so that no caller needs to import
    from the users domain.

    Attributes:
        _repository: The users domain repository used for the lookup.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialise the adapter with a database session.

        Args:
            session: Async SQLModel session injected per request.
        """
        self._repository = UserRepository(session=session)

    async def __call__(self, user_id: str) -> UserContractResult | None:
        """Retrieve a user by its ULID.

        Args:
            user_id: ULID of the user to look up.

        Returns:
            UserContractResult if the user exists, None otherwise.
        """
        entity = await self._repository.get_by_id(user_id)
        if entity is None:
            return None
        return UserContractResult(
            id=entity.id,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            document_type=entity.document_type,
            document_number=entity.document_number,
            is_superadmin=entity.is_superadmin,
        )


def build_get_user_by_id_adapter(
    session: PostgresSessionDependency,
) -> GetUserByIdAdapter:
    """Construct a GetUserByIdAdapter with an injected session.

    Args:
        session: Async database session provided by FastAPI.

    Returns:
        GetUserByIdAdapter: Ready-to-use adapter instance.
    """
    return GetUserByIdAdapter(session=session)


GetUserByIdDependency = Annotated[
    GetUserByIdAdapter,
    Depends(build_get_user_by_id_adapter),
]
