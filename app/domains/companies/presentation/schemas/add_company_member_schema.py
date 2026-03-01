"""Add company member request schema."""

from pydantic import BaseModel

from app.shared.auth.role import Role


class AddCompanyMemberRequestSchema(BaseModel):
    """Request body for POST /api/v1/companies/{company_id}/members.

    Attributes:
        user_id: ULID of the user to add as a member.
        role: Permission level to assign. Defaults to MEMBER.
    """

    user_id: str
    role: Role = Role.MEMBER
