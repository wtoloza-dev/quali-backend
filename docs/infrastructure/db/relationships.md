# Database Relationships Diagram

All relationships are enforced at the **application layer** (no FK constraints in DB).
Arrows show logical references: `child.field` -> `parent.table`.

## Entity Relationship Diagram (Mermaid)

```mermaid
erDiagram
    users {
        str id PK "Firebase UID"
        str first_name
        str last_name
        str email UK
        str document_type
        str document_number
        bool is_superadmin
    }

    companies {
        str id PK "ULID"
        str name
        str slug UK
        str company_type
        str email
        str country
    }

    company_members {
        str id PK "ULID"
        str company_id FK
        str user_id FK
        str role
    }

    courses {
        str id PK "ULID"
        str company_id FK
        str title
        str slug UK
        str vertical
        int validity_days
        str visibility
        str status
    }

    course_modules {
        str id PK "ULID"
        str course_id FK
        str title
        int order
        int passing_score
        int max_attempts
    }

    course_lessons {
        str id PK "ULID"
        str module_id FK
        str title
        json content
        int order
        bool is_preview
    }

    enrollments {
        str id PK "ULID"
        str user_id FK
        str course_id FK
        str status
        str access_type
        datetime enrolled_at
        datetime completed_at
    }

    assessment_questions {
        str id PK "ULID"
        str course_id FK
        str module_id FK
        str question_type
        json config
    }

    assessment_attempts {
        str id PK "ULID"
        str enrollment_id FK
        str module_id FK
        int score
        bool passed
        int attempt_number
    }

    certificates {
        str id PK "ULID"
        str company_id FK
        str recipient_id FK
        str title
        str token UK
        str status "computed"
        datetime issued_at
        datetime expires_at
    }

    access_codes {
        str id PK "ULID"
        str code UK
        str course_id FK
        str redeemed_by FK
        str enrollment_id FK
        bool is_redeemed
    }

    training_plans {
        str id PK "ULID"
        str company_id FK
        int year
        str title
        str status
    }

    training_plan_items {
        str id PK "ULID"
        str plan_id FK
        str course_id FK
        date scheduled_date
    }

    legal_acceptances {
        str id PK "ULID"
        str user_id FK
        str enrollment_id FK
        str acceptance_type
        str declaration_text
    }

    entity_tombstones {
        str id PK "ULID"
        str entity_type
        str entity_id
        json payload
        datetime deleted_at
    }

    %% ── Tenant hierarchy ──
    companies ||--o{ company_members : "has members"
    users ||--o{ company_members : "belongs to companies"

    %% ── Course structure ──
    companies ||--o{ courses : "owns"
    courses ||--o{ course_modules : "contains"
    course_modules ||--o{ course_lessons : "contains"

    %% ── Enrollment lifecycle ──
    users ||--o{ enrollments : "enrolls in"
    courses ||--o{ enrollments : "enrolled by"
    enrollments ||--o{ assessment_attempts : "produces"
    course_modules ||--o{ assessment_attempts : "assessed by"

    %% ── Assessments ──
    courses ||--o{ assessment_questions : "has"
    course_modules ||--o{ assessment_questions : "scoped to"

    %% ── Certification ──
    companies ||--o{ certificates : "issues"
    users ||--o{ certificates : "receives"

    %% ── Access codes ──
    courses ||--o{ access_codes : "redeemable for"

    %% ── Training plans ──
    companies ||--o{ training_plans : "plans"
    training_plans ||--o{ training_plan_items : "includes"
    courses ||--o{ training_plan_items : "scheduled in"

    %% ── Legal ──
    users ||--o{ legal_acceptances : "accepts"
    enrollments ||--o{ legal_acceptances : "requires"
```

---

## Relationship Summary Table

| Parent | Child | Join | Cardinality | Notes |
|--------|-------|------|-------------|-------|
| `companies` | `company_members` | `company_members.company_id = companies.id` | 1:N | UNIQUE(company_id, user_id) |
| `users` | `company_members` | `company_members.user_id = users.id` | 1:N | Same row, double reference |
| `companies` | `courses` | `courses.company_id = companies.id` | 1:N | Tenant-scoped catalog |
| `courses` | `course_modules` | `course_modules.course_id = courses.id` | 1:N | Ordered by `order` |
| `course_modules` | `course_lessons` | `course_lessons.module_id = course_modules.id` | 1:N | Ordered by `order` |
| `users` | `enrollments` | `enrollments.user_id = users.id` | 1:N | |
| `courses` | `enrollments` | `enrollments.course_id = courses.id` | 1:N | UNIQUE(user_id, course_id) |
| `enrollments` | `assessment_attempts` | `assessment_attempts.enrollment_id = enrollments.id` | 1:N | |
| `course_modules` | `assessment_attempts` | `assessment_attempts.module_id = course_modules.id` | 1:N | Nullable (legacy) |
| `courses` | `assessment_questions` | `assessment_questions.course_id = courses.id` | 1:N | |
| `course_modules` | `assessment_questions` | `assessment_questions.module_id = course_modules.id` | 1:N | Nullable |
| `companies` | `certificates` | `certificates.company_id = companies.id` | 1:N | Tenant-scoped |
| `users` | `certificates` | `certificates.recipient_id = users.id` | 1:N | |
| `courses` | `access_codes` | `access_codes.course_id = courses.id` | 1:N | |
| `users` | `access_codes` | `access_codes.redeemed_by = users.id` | 1:N | Nullable |
| `enrollments` | `access_codes` | `access_codes.enrollment_id = enrollments.id` | 1:1 | Created on redemption |
| `companies` | `training_plans` | `training_plans.company_id = companies.id` | 1:N | |
| `training_plans` | `training_plan_items` | `training_plan_items.plan_id = training_plans.id` | 1:N | |
| `courses` | `training_plan_items` | `training_plan_items.course_id = courses.id` | 1:N | |
| `users` | `legal_acceptances` | `legal_acceptances.user_id = users.id` | 1:N | |
| `enrollments` | `legal_acceptances` | `legal_acceptances.enrollment_id = enrollments.id` | 1:N | |

---

## Key Design Decisions

### Why no FK constraints?

1. **Cross-domain independence** — each domain owns its tables and can be deployed/migrated independently
2. **Soft-coupled via ULID references** — referential integrity enforced at the application layer (use cases validate existence before writes)
3. **Hard delete + tombstone** — deleted entities leave a JSON snapshot in `entity_tombstones`, no cascading deletes needed
4. **Firebase UID as user ID** — `users.id` is a Firebase UID (not ULID), making it awkward for standard FK constraints

### Scalability considerations

| Aspect | Current design | Risk | Mitigation |
|--------|---------------|------|------------|
| **Tenant isolation** | `company_id` column + app-level filtering | Query without `company_id` returns cross-tenant data | Always include `company_id` in WHERE; add composite indexes if needed |
| **JSON columns** | `content`, `config`, `answers` | Not queryable by default | Only used for display/snapshot, never for filtering |
| **No cascading deletes** | Tombstone pattern | Orphaned rows possible if app bug | Periodic cleanup scripts; tombstone gives audit trail |
| **Single enrollments table** | All enrollment types in one table | High write volume per course launch | Indexed on `(user_id, course_id)`; partitioning not needed yet |
| **Assessment attempts** | Append-only | Grows linearly with usage | Indexed on `enrollment_id`; archive old attempts if needed |

### Entity count: 16 tables

```
Core:        users, companies, company_members (3)
Education:   courses, course_modules, course_lessons,
             enrollments, assessment_questions, assessment_attempts,
             access_codes, training_plans, training_plan_items (9)
Cert:        certificates (1)
Legal:       legal_acceptances (1)
System:      entity_tombstones (1)
IAM:         roles live in company_members.role (no separate table)
```
