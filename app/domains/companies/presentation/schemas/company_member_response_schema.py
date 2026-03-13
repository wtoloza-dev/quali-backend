"""Company member response schema."""

from datetime import datetime

from pydantic import BaseModel

from app.shared.auth.role import Role


class CompanyMemberResponseSchema(BaseModel):
    """Serialized company membership data.

    Attributes:
        id: ULID of the membership record.
        company_id: ULID of the company.
        user_id: ULID of the user.
        role: Permission level within the company.
        created_at: Timestamp when the membership was created.
        created_by: ID of the actor who created the membership.
    """

    id: str
    company_id: str
    user_id: str
    role: Role
    created_at: datetime
    created_by: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
