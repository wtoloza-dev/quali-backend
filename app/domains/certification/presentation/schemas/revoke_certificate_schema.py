"""Revoke certificate request schema."""

from pydantic import BaseModel


class RevokeCertificateRequestSchema(BaseModel):
    """Input schema for the revoke certificate endpoint.

    Attributes:
        reason: Mandatory reason explaining why the certificate is being revoked.
    """

    reason: str
