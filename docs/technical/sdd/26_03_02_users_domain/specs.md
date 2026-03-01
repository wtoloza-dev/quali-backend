# Users Domain + Company Members — Functional Specifications

## Users Domain
Manages user profiles independently of any company.

### User Entity
| Field      | Type     | Notes                      |
|------------|----------|----------------------------|
| id         | str      | ULID, auto                 |
| first_name | str      | required                   |
| last_name  | str      | required                   |
| email      | str      | unique among active users  |
| + audit fields (AuditEntity) |       |

### Business Rules
1. Email is unique among non-deleted users.
2. Email is immutable after creation (identity field).
3. Soft-deleted users are invisible to all queries.

### API
| Method | Path                    | Status | Description      |
|--------|-------------------------|--------|------------------|
| POST   | /api/v1/users/          | 201    | Create user      |
| GET    | /api/v1/users/{id}      | 200    | Get user by ID   |
| PATCH  | /api/v1/users/{id}      | 200    | Update user      |
| DELETE | /api/v1/users/{id}      | 204    | Soft-delete user |

### Response Schemas
- UserPublicResponseSchema: id, first_name, last_name, created_at
- UserPrivateResponseSchema: all fields including email and audit data

---

## Company Members (extension of companies domain)
A company manages its own member list.

### CompanyMember Entity
| Field      | Type | Notes                    |
|------------|------|--------------------------|
| id         | str  | ULID, auto               |
| company_id | str  | plain string, no FK      |
| user_id    | str  | plain string, no FK      |
| + audit fields             |                          |

### Business Rules
1. A (company_id, user_id) pair must be unique among active memberships.
2. No physical FK constraints — referential integrity is application-level.
3. Memberships are soft-deleted on removal.

### API
| Method | Path                                           | Status | Description           |
|--------|------------------------------------------------|--------|-----------------------|
| POST   | /api/v1/companies/{id}/members                 | 201    | Add user to company   |
| GET    | /api/v1/companies/{id}/members                 | 200    | List company members  |
| DELETE | /api/v1/companies/{id}/members/{user_id}       | 204    | Remove member         |
