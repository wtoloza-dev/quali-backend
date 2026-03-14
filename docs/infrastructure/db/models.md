# Database Models Reference

All models use **ULID as `str`** for IDs, **no FK constraints** at DB level (enforced in application code), and **`sa.String()`** for enums (never PG enum types).

---

## Shared

### AuditModel (base mixin — not a table)

Every domain model inherits these fields:

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID, auto-generated |
| `created_at` | `datetime(tz)` | `server_default=now()` |
| `created_by` | `str` | ULID of creator, required |
| `updated_at` | `datetime(tz)` | `server_default=now()`, `onupdate=now()` — never set in Python |
| `updated_by` | `str \| None` | ULID of last updater |

### `entity_tombstones`

Stores full JSON snapshots of hard-deleted entities.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `entity_type` | `str` | e.g. `"company"`, `"certificate"` — indexed |
| `entity_id` | `str` | ULID of deleted entity — indexed |
| `payload` | `JSON` | Full snapshot before deletion |
| `deleted_at` | `datetime(tz)` | When it was deleted |
| `deleted_by` | `str` | Who deleted it |

---

## Users Domain

### `users`

Global user registry. ID is Firebase UID (not ULID).

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | Firebase UID (not ULID) |
| `first_name` | `str` | Required — starts as `""` on registration, filled later in profile |
| `last_name` | `str` | Required — starts as `""` on registration, filled later in profile |
| `email` | `str` | **Unique**, indexed |
| `document_type` | `str \| None` | CC, CE, TI, PP, NIT |
| `document_number` | `str \| None` | Encrypted (Fernet) |
| `is_superadmin` | `bool` | Default `false` |
| + audit fields | | |

**Constraints:** `UNIQUE(email)`

---

## Companies Domain

### `companies`

Tenant root entity.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `name` | `str` | Display name |
| `slug` | `str` | **Unique**, indexed, immutable |
| `company_type` | `str` | `personal` \| `organization` |
| `email` | `str` | Contact email |
| `country` | `str` | Enum (e.g. `CO`) |
| `legal_name` | `str \| None` | |
| `logo_url` | `str \| None` | |
| `tax_type` | `str \| None` | `NIT` \| `CC` \| etc. |
| `tax_id` | `str \| None` | |
| + audit fields | | |

**Constraints:** `UNIQUE(slug)`

### `company_members`

Maps users to companies with roles (RBAC).

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `company_id` | `str` | -> `companies.id` — indexed |
| `user_id` | `str` | -> `users.id` — indexed |
| `role` | `str` | `viewer` \| `member` \| `admin` \| `owner` |
| + audit fields | | |

**Constraints:** `UNIQUE(company_id, user_id)`

---

## Certification Domain

### `certificates`

Digital certificates issued to users.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `company_id` | `str` | -> `companies.id` — indexed |
| `recipient_id` | `str` | -> `users.id` — indexed |
| `title` | `str` | Course title at issuance time |
| `description` | `str \| None` | Course description at issuance time |
| `token` | `str` | **Unique**, indexed — ULID for QR verification |
| `issued_at` | `datetime(tz)` | |
| `expires_at` | `datetime(tz) \| None` | Computed: `issued_at + course.validity_days` |
| `revoked_at` | `datetime(tz) \| None` | |
| `revoked_by` | `str \| None` | -> `users.id` |
| `revoked_reason` | `str \| None` | Required when revoking |
| + audit fields | | |

**Constraints:** `UNIQUE(token)`
**Computed (app):** `status` = `revoked` if `revoked_at`, `expired` if past `expires_at`, else `active`

---

## Education Domain — Courses

### `courses`

Course catalog. Tenant-scoped.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `company_id` | `str` | -> `companies.id` — indexed |
| `title` | `str` | |
| `slug` | `str` | **Unique**, indexed, immutable |
| `description` | `str \| None` | |
| `vertical` | `str` | `food_quality` \| `sst` \| `general` |
| `regulatory_ref` | `str \| None` | e.g. "Resolución 2674 de 2013" |
| `validity_days` | `int \| None` | Certificate validity period |
| `visibility` | `str` | `public` \| `private` |
| `status` | `str` | `draft` \| `published` \| `archived` |
| + audit fields | | |

**Constraints:** `UNIQUE(slug)`

### `course_modules`

Ordered modules within a course. Each module has its own assessment config.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `course_id` | `str` | -> `courses.id` — indexed |
| `title` | `str` | |
| `order` | `int` | 1-based, ascending |
| `passing_score` | `int` | Default `80` (0-100) |
| `max_attempts` | `int` | Default `3` |
| + audit fields | | |

### `course_lessons`

Ordered lessons within a module. Content is a JSON array of typed blocks.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `module_id` | `str` | -> `course_modules.id` — indexed |
| `title` | `str` | |
| `content` | `JSON` | Array of `ContentBlock` objects |
| `order` | `int` | 1-based, ascending |
| `is_preview` | `bool` | Default `false` — free content without enrollment |
| + audit fields | | |

---

## Education Domain — Enrollments

### `enrollments`

User enrollment in a course. One enrollment per user/course pair.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `user_id` | `str` | -> `users.id` — indexed |
| `course_id` | `str` | -> `courses.id` — indexed |
| `is_mandatory` | `bool` | Default `false` |
| `status` | `str` | `not_started` \| `in_progress` \| `completed` \| `failed` \| `dropped` |
| `access_type` | `str` | `company_enrollment` \| `purchase` \| `subscription` \| `preview` |
| `enrolled_at` | `datetime(tz)` | |
| `completed_at` | `datetime(tz) \| None` | |
| `start_date` | `datetime(tz) \| None` | When full access begins |
| `end_date` | `datetime(tz) \| None` | When full access expires |
| + audit fields | | |

**Constraints:** `UNIQUE(user_id, course_id)`

---

## Education Domain — Assessments

### `assessment_questions`

Question bank. Scoped to course, optionally to a module.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `course_id` | `str` | -> `courses.id` — indexed |
| `module_id` | `str \| None` | -> `course_modules.id` — indexed |
| `text` | `str` | Question text |
| `question_type` | `str` | `multiple_choice` \| `true_false` \| `short_answer` \| `matching` \| `dropdown` \| `multi_select` |
| `config` | `JSON` | Type-specific options, answers, etc. |
| `randomize` | `bool` | Default `true` |
| `order` | `int` | Default `0` |
| + audit fields | | |

### `assessment_attempts`

Immutable exam attempt records.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `enrollment_id` | `str` | -> `enrollments.id` — indexed |
| `module_id` | `str \| None` | -> `course_modules.id` — indexed |
| `score` | `int` | 0-100 |
| `passed` | `bool` | `score >= module.passing_score` |
| `attempt_number` | `int` | 1-based |
| `answers` | `JSON` | Snapshot of submitted answers |
| `correct_question_ids` | `JSON` | List of correctly answered question IDs |
| `taken_at` | `datetime(tz)` | |
| + audit fields | | |

---

## Education Domain — Access Codes

### `access_codes`

One-time redemption codes for course enrollment.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `code` | `str` | **Unique**, indexed — format `QUALI-XXXX-XXXX` |
| `course_id` | `str` | -> `courses.id` — indexed |
| `is_redeemed` | `bool` | Default `false` |
| `redeemed_by` | `str \| None` | -> `users.id` |
| `redeemed_at` | `datetime(tz) \| None` | |
| `enrollment_id` | `str \| None` | -> `enrollments.id` — indexed |
| + audit fields | | |

**Constraints:** `UNIQUE(code)`

---

## Education Domain — Training Plans

### `training_plans`

Annual training plans per company.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `company_id` | `str` | -> `companies.id` — indexed |
| `year` | `int` | Calendar year |
| `title` | `str` | |
| `status` | `str` | `draft` \| `active` \| `completed` \| `archived` |
| + audit fields | | |

### `training_plan_items`

Courses scheduled within a training plan.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `plan_id` | `str` | -> `training_plans.id` — indexed |
| `course_id` | `str` | -> `courses.id` — indexed |
| `target_role` | `str \| None` | |
| `scheduled_date` | `date \| None` | |
| `notes` | `str \| None` | |
| + audit fields | | |

---

## Legal Domain

### `legal_acceptances`

Write-only audit log. Never updated or deleted. Does NOT inherit AuditModel.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` PK | ULID |
| `user_id` | `str` | -> `users.id` — indexed |
| `enrollment_id` | `str` | -> `enrollments.id` — indexed |
| `acceptance_type` | `str` | e.g. `enrollment_identity` |
| `declaration_text` | `str` | Full legal text that was accepted |
| `ip_address` | `str \| None` | Client IP at acceptance time |
| `accepted_at` | `datetime(tz)` | `server_default=now()` |
