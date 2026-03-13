"""get_user_by_id contract port.

Defines the minimal interface and return type for retrieving a user by ID
across domain boundaries. Any domain that needs to look up a user depends
only on this module — never on the users domain directly.
"""

from typing import Protocol

from pydantic import BaseModel


class UserContractResult(BaseModel):
    """Minimal user projection returned by the get_user_by_id contract.

    Contains only the fields that cross-domain consumers are allowed to
    observe. Source-domain internals (audit fields, etc.) are not exposed.

    Attributes:
        id: ULID of the user.
        email: Primary contact email.
        first_name: User's given name.
        last_name: User's family name.
    """

    id: str
    email: str
    first_name: str
    last_name: str
    document_type: str | None = None
    document_number: str | None = None
    is_superadmin: bool = False


class GetUserByIdPort(Protocol):
    """Contract interface for fetching a user by ULID.

    Implemented by GetUserByIdAdapter in the infrastructure layer.
    Consumers (e.g. certification use cases) depend on this Protocol,
    making them testable with any fake that satisfies the interface.
    """

    async def __call__(self, user_id: str) -> UserContractResult | None:
        """Retrieve a user by its ULID.

        Args:
            user_id: ULID of the user to look up.

        Returns:
            UserContractResult if the user exists, None otherwise.
        """
        ...
