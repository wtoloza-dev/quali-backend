"""Certificate SQLModel ORM model."""

from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field

from app.shared.models.audit_model import AuditModel


class CertificateModel(AuditModel, table=True):
    """SQLModel ORM representation of the certificates table.

    Maps the certificate data to the database. Used exclusively within
    the infrastructure layer — never returned directly to the application
    or presentation layers.

    Attributes:
        __tablename__: Database table name.
        company_id: Tenant that issued the certificate (indexed).
        recipient_id: User who received the certificate (indexed).
        title: Human-readable name of the certificate.
        description: Optional longer description.
        token: Unique ULID token for QR verification (indexed, unique).
        issued_at: Timestamp when the certificate was officially issued.
        expires_at: Optional expiration timestamp.
        revoked_at: Timestamp of revocation, if applicable.
        revoked_by: ID of the user who revoked the certificate.
        revoked_reason: Reason provided for the revocation.
    """

    __tablename__ = "certificates"

    company_id: str = Field(nullable=False, index=True)
    recipient_id: str = Field(nullable=False, index=True)
    title: str = Field(nullable=False)
    description: str | None = Field(default=None, nullable=True)
    token: str = Field(nullable=False, unique=True, index=True)
    issued_at: datetime = Field(
        nullable=False,
        sa_type=DateTime(timezone=True),
    )
    expires_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
    revoked_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
    revoked_by: str | None = Field(default=None, nullable=True)
    revoked_reason: str | None = Field(default=None, nullable=True)
