"""Generate access codes request schema."""

from pydantic import BaseModel, Field


class GenerateAccessCodesRequestSchema(BaseModel):
    """Request body for generating access codes.

    Attributes:
        quantity: Number of access codes to generate.
    """

    quantity: int = Field(gt=0, le=500)
