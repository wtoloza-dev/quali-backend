"""save_legal_acceptance contract port.

Defines the minimal interface and input type for persisting a legal
acceptance record across domain boundaries. The education domain uses
this contract so it never imports from the legal domain directly.
"""

from typing import Protocol

from pydantic import BaseModel


class LegalAcceptanceContractInput(BaseModel):
    """Input DTO for saving a legal acceptance record.

    Attributes:
        user_id: ULID of the user who accepted.
        enrollment_id: ULID of the enrollment this acceptance is tied to.
        acceptance_type: Category of declaration (e.g. "enrollment_identity").
        declaration_text: The exact legal text the user accepted.
        ip_address: Client IP at the time of acceptance, if available.
    """

    user_id: str
    enrollment_id: str
    acceptance_type: str
    declaration_text: str
    ip_address: str | None = None


class SaveLegalAcceptancePort(Protocol):
    """Contract interface for persisting a legal acceptance record."""

    async def __call__(self, data: LegalAcceptanceContractInput) -> None:
        """Save a legal acceptance record.

        Args:
            data: The acceptance data to persist.
        """
        ...
