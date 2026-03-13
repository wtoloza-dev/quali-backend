"""User domain entity."""

from pydantic import BaseModel

from app.shared.entities import AuditEntity


class UserData(BaseModel):
    """Lean user data used by use cases that create a user.

    Attributes:
        first_name: The user's given name.
        last_name: The user's family name.
        email: Primary contact email; unique across active users.
        document_type: Type of ID document (CC, CE, TI, PP, NIT).
        document_number: ID document number (stored encrypted).
    """

    first_name: str
    last_name: str
    email: str
    document_type: str | None = None
    document_number: str | None = None
    is_superadmin: bool = False


class UserEntity(UserData, AuditEntity):
    """Full user entity returned by the repository after persistence.

    Combines the domain fields from UserData with the audit fields
    from AuditEntity. Use cases receive UserData as input and
    UserEntity as output from the repository.
    """

    pass
