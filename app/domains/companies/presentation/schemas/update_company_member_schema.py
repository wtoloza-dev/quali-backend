"""Update company member request schema."""

from pydantic import BaseModel

from app.shared.auth.role import Role


class UpdateCompanyMemberRequestSchema(BaseModel):
    """Request body for PATCH /api/v1/companies/{company_id}/members/{user_id}.

    Attributes:
        role: The new permission level to assign to the member.
    """

    role: Role
