"""save_legal_acceptance contract — port, input DTO, and adapter."""

from .save_legal_acceptance_adapter import (
    SaveLegalAcceptanceAdapter,
    SaveLegalAcceptanceDependency,
)
from .save_legal_acceptance_port import (
    LegalAcceptanceContractInput,
    SaveLegalAcceptancePort,
)


__all__ = [
    "SaveLegalAcceptancePort",
    "LegalAcceptanceContractInput",
    "SaveLegalAcceptanceAdapter",
    "SaveLegalAcceptanceDependency",
]
