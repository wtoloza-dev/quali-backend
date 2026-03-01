"""Company member domain entity."""

from pydantic import BaseModel

from app.shared.auth.role import Role
from app.shared.entities import AuditEntity


class CompanyMemberData(BaseModel):
    """Lean company member data used by use cases that add a member.

    Attributes:
        company_id: ULID of the company being joined.
        user_id: ULID of the user being added as a member.
        role: Permission level within the company. Defaults to MEMBER.
    """

    company_id: str
    user_id: str
    role: Role = Role.MEMBER


class CompanyMemberEntity(CompanyMemberData, AuditEntity):
    """Full company member entity returned by the repository after persistence.

    Combines the domain fields from CompanyMemberData with the audit fields
    from AuditEntity. No physical FK constraints — referential integrity is
    enforced at the application level.
    """

    pass
