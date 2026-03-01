"""Role enum and hierarchy — shared across all domains.

Originally defined in the IAM domain, moved to shared/ because every
domain that uses require_role() or stores a role value needs these
definitions.
"""

from enum import StrEnum


class Role(StrEnum):
    """Permission levels within a company tenant.

    Ordered from highest to lowest privilege. The hierarchy is used
    by require_role() to allow higher roles to pass lower-level guards.

    Attributes:
        OWNER: Full control. Can manage members, roles, and delete the company.
        ADMIN: Can manage resources and members. Cannot delete the company.
        MEMBER: Standard access. Can create and read resources.
        VIEWER: Read-only access.
    """

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


# Maps each role to a numeric weight for hierarchy comparison.
# A role with a higher weight satisfies guards for lower-weight roles.
#
# Weights are spaced by 10 so new roles can be inserted between existing
# ones by picking a value in the gap — never renumber existing entries.
# Example: add SUPERVISOR between MEMBER and ADMIN → assign weight 25.
ROLE_HIERARCHY: dict[Role, int] = {
    Role.VIEWER: 10,
    Role.MEMBER: 20,
    Role.ADMIN: 30,
    Role.OWNER: 40,
}
