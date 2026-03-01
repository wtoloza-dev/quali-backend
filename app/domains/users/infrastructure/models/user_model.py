"""User SQLModel ORM model."""

from sqlmodel import Field

from app.shared.models import AuditModel


class UserModel(AuditModel, table=True):
    """SQLModel ORM representation of the users table.

    Maps the user data to the database. Used exclusively within
    the infrastructure layer — never returned directly to the application
    or presentation layers.

    Attributes:
        __tablename__: Database table name.
        first_name: The user's given name.
        last_name: The user's family name.
        email: Primary contact email; unique among active users, indexed for fast lookups.
    """

    __tablename__ = "users"

    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(nullable=False, index=True, unique=True)
    document_type: str | None = Field(default=None, nullable=True)
    document_number: str | None = Field(default=None, nullable=True)
