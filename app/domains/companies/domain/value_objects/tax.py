"""Tax value object."""

from pydantic import BaseModel

from ..enums import TaxType


class Tax(BaseModel):
    """Represents a company's tax identification.

    Immutable value object. Two Tax instances with the same tax_type
    and tax_id are considered equal regardless of identity.

    Attributes:
        tax_type: The type of tax identifier (e.g. NIT for Colombia).
        tax_id: The actual tax identifier number issued by the authority.
    """

    model_config = {"frozen": True}

    tax_type: TaxType
    tax_id: str
