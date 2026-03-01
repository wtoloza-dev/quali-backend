"""Redeem access code request schema."""

from pydantic import BaseModel


class RedeemAccessCodeRequestSchema(BaseModel):
    """Request body for redeeming an access code.

    Attributes:
        code: The access code string to redeem (QUALI-XXXX-XXXX format).
    """

    code: str
