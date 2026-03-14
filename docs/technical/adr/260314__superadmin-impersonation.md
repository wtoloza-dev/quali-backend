# ADR: Superadmin Impersonation (Option 3 — Shadow AuthContext)

**Date:** 2026-03-14
**Status:** Accepted
**Author:** William Toloza

---

## Context

Quali is a compliance and professional training platform. Support and debugging scenarios require superadmins to view the system from a specific user's perspective — for example, to reproduce enrollment issues, verify course access, or troubleshoot assessment flows.

Without impersonation, superadmins must either query the database directly or ask the user to share their screen, both of which are slow and error-prone.

### Constraints

- The backend uses Firebase JWT authentication with no service account (stateless verification only).
- The `AuthMiddleware` is a pure ASGI middleware with no database access.
- Colombian data protection law (Ley 1581 de 2012) requires a legitimate purpose and audit trail for accessing user data.

---

## Decision

Implement **Option 3: Shadow AuthContext** — a header-based impersonation mechanism that preserves both the real and impersonated identities throughout the request lifecycle.

### Mechanism

1. Superadmin sends their own Firebase JWT in `Authorization: Bearer <token>` plus an `X-Impersonate-User: <target_user_ulid>` header.
2. A new FastAPI dependency (`ImpersonatedUserDependency`) verifies the caller is a superadmin via the `GetUserByIdPort` contract (`is_superadmin` field).
3. If verified, the dependency returns an `AuthContext` with:
   - `user_id` = impersonated user (effective identity for business logic)
   - `email` = impersonated user's email
   - `real_user_id` = superadmin's ULID (for audit)
4. If the caller is not a superadmin, or the target user does not exist, the request is rejected with `403 Forbidden`.

### AuthContext Changes

```python
class AuthContext(BaseModel):
    user_id: str               # effective user (impersonated or real)
    email: str
    real_user_id: str | None   # superadmin ULID when impersonating

    @property
    def is_impersonating(self) -> bool: ...

    @property
    def audit_user_id(self) -> str:
        """Always returns the real actor for audit fields."""
        return self.real_user_id or self.user_id
```

### Opt-in Per Route

Impersonation is not global. Routes that support it must explicitly use `ImpersonatedUserDependency` instead of `CurrentUserDependency`. Routes using `CurrentUserDependency` ignore the header entirely.

```python
from app.shared.auth.impersonation import ImpersonatedUserDependency

@router.get("/enrollments")
async def handle_list_enrollments(
    auth: ImpersonatedUserDependency,
) -> ...:
```

### Circular Import Prevention

`impersonation.py` imports from `app.shared.contracts.get_user_by_id.get_user_by_id_adapter` (direct path) and is **NOT re-exported** from `app.shared.auth.__init__` — same pattern as `require_role`.

---

## Alternatives Considered

### Option 1: Simple Header Swap

Replace `user_id` in context when `X-Impersonate-User` is present (superadmin only). Discard the admin's identity entirely.

**Rejected because:** No audit trail of who performed the impersonation. Violates the Colombian data protection requirement for traceability.

### Option 2: Firebase Custom Token Minting

Use Firebase Admin SDK to generate a short-lived token for the target user. The admin uses this real Firebase token.

**Rejected because:** Requires a Firebase service account, which the backend currently does not use. Adds infrastructure complexity (secret management, key rotation). Also creates a real authentication session for a user who did not initiate it, which has legal implications.

---

## Consequences

### Positive

- **Full audit trail:** `real_user_id` is always available for logging and audit fields (`created_by`, `updated_by`).
- **No infrastructure changes:** Works with the existing stateless Firebase JWT flow.
- **Opt-in:** Only routes that explicitly use `ImpersonatedUserDependency` support it — no risk of accidental impersonation on sensitive endpoints.
- **Testable:** `ImpersonatedUserDependency` is a standard FastAPI dependency, overridable in tests.

### Negative

- **Two dependency types:** Developers must choose between `CurrentUserDependency` and `ImpersonatedUserDependency`. Wrong choice = silent failure (header ignored) or unintended impersonation.
- **Extra DB query:** Each impersonated request queries the users table to verify `is_superadmin`, even though the middleware already decoded the JWT. Acceptable at superadmin-only scale.

### Risks

- **Superadmin compromise:** If a superadmin account is compromised, the attacker can impersonate any user. Mitigation: restrict `is_superadmin` to a minimal set of users; monitor impersonation logs for anomalies.
- **Legal compliance:** Impersonation must be disclosed in the platform's privacy policy and terms of service. Action item: update legal documents before enabling in production.

---

## Implementation

| File | Description |
|------|-------------|
| `app/shared/auth/auth_context.py` | Added `real_user_id`, `is_impersonating`, `audit_user_id` |
| `app/shared/auth/impersonation.py` | New — `get_impersonated_user` dependency + `ImpersonatedUserDependency` |

### Logging

Every impersonation is logged at `WARNING` level:

```
Impersonation active: superadmin 01ADMIN... acting as user 01TARGET... (target@email.com)
```

### Client Usage

```
GET /api/v1/companies/{id}/education/enrollments/
Authorization: Bearer <superadmin's Firebase JWT>
X-Impersonate-User: 01TARGETUSERULID
```
