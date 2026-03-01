# Phase 0 — Foundation

## Goal

Establish the core infrastructure that every subsequent phase depends on. Nothing meaningful can be built on a shaky foundation, and retrofitting multi-tenancy, RBAC, or industry configuration into a running platform is one of the most expensive mistakes a SaaS project can make.

This phase is not user-facing. It delivers no product features. It delivers **the skeleton everything else plugs into**, and it must be designed with two verticals in mind from the first commit: occupational safety (SST) and food quality.

---

## Scope

### Multi-tenancy

Every resource in Quali belongs to a company (tenant). This must be enforced at the data layer from day one. There are no global resources except the standards library and platform configuration.

- `Company` model with fully isolated data scope.
- All queries filtered by `company_id` enforced at the repository or middleware layer — no route should be able to access another tenant's data.
- Slug-based tenant identification (`acme.quali.app` or `/t/acme/`).
- A company can belong to one or more industry verticals (SST, food quality, or both).

### Industry Vertical Configuration

When a company is onboarded, they select which verticals and standards apply to them. This configuration drives:

- Which modules are visible in their dashboard.
- Which standards appear in the compliance library.
- Which course templates are pre-loaded.
- Which regulatory calendar deadlines are tracked.

```
CompanyVertical
  company_id    FK → Company
  vertical      enum: sst | food_quality | general_quality | [future]
  active        bool

CompanyStandard
  company_id    FK → Company
  standard_id   FK → Standard
  adopted_at    date
```

### Authentication & Authorization

- JWT-based authentication with refresh token rotation.
- Role-Based Access Control (RBAC) with roles designed for both verticals from the start:

| Role | Description |
|---|---|
| `admin` | Full company administration |
| `sst_coordinator` | Manages the SG-SST system |
| `quality_manager` | Manages food/general quality system |
| `hseq_manager` | Manages both SST and quality (common in Colombian companies) |
| `trainer` | Creates and manages courses |
| `auditor` | Executes audits (internal or external) |
| `employee` | Takes courses, receives certificates, reports incidents |
| `copasst_member` | COPASST committee member (SST-specific role) |

- Permissions scoped per tenant — a user can have different roles in different companies (e.g., an external auditor).
- A user's accessible modules are filtered by both their role and the company's active verticals.

### User Management

- Invite-based onboarding (no public sign-up — this is a B2B platform).
- User profile: name, position, department, ARL affiliation (relevant for SST reporting).
- Password reset and email verification flows.
- Bulk user import via CSV (essential for companies onboarding 50–500 employees at once).

### Colombian Regulatory Calendar

A first-class feature, not an afterthought. The platform knows the mandatory annual deliverables defined by **Resolución 0312 de 2019** (SST) and **Resolución 2674 de 2013** (food), filtered by company size and risk level.

Examples of tracked deadlines:
- Annual SST management review
- COPASST committee elections (every 2 years)
- Occupational health medical examinations
- Emergency plan drill (at least once per year)
- INVIMA sanitary concept renewal

The dashboard surfaces upcoming deadlines and flags overdue ones.

```
RegulatoryEvent
  id              UUID
  company_id      FK → Company
  standard_id     FK → Standard
  title           string
  description     text
  due_date        date
  recurrence      enum: annual | biannual | once | custom
  status          enum: pending | completed | overdue
  evidence_file   string | null
```

### Core API Infrastructure

- Versioned API (`/api/v1/`).
- Standardized error response format in Spanish (for client-facing messages) and English (for developer logs).
- Request validation via Pydantic.
- Health check endpoint (`/health`).
- Structured JSON logging with request tracing.
- Rate limiting on auth endpoints.

### Developer Tooling

- Database migrations via Alembic.
- Docker Compose for local development (API + PostgreSQL + Redis).
- Environment configuration via `pydantic-settings` and `.env`.
- CI pipeline skeleton (GitHub Actions): lint → test → build.
- Seed script to populate standards library and demo company data.

---

## Data Model (draft, core entities)

```
Company
  id              UUID
  name            string
  slug            string (unique)
  nit             string (Colombian tax ID)
  size            enum: micro | small | medium | large
  risk_level      enum: i | ii | iii | iv  (Res. 0312 classification)
  arl             string | null
  industry        string
  created_at      datetime

User
  id              UUID
  email           string (unique)
  full_name       string
  position        string | null
  department      string | null
  is_active       bool

UserCompany
  user_id         FK → User
  company_id      FK → Company
  role            enum (see roles above)
  joined_at       datetime
```

---

## Why This Comes First

Without multi-tenancy, RBAC, and vertical configuration in place:

- Every feature built in Phases 1–6 will need to be revisited to add tenant isolation — a security risk and a technical debt that compounds fast.
- Roles designed only for food quality will need to be broken and rebuilt when SST is added.
- Regulatory calendar logic added late will require retroactive data for existing tenants.

The cost of doing this right in Phase 0 is low. The cost of fixing it in Phase 3 is very high.

---

## Success Criteria

- A company can be onboarded with industry vertical selection.
- Users can be invited, authenticated, and assigned roles.
- All API routes enforce tenant isolation — no cross-tenant data access is possible.
- The regulatory calendar surfaces upcoming SST and food compliance deadlines.
- A new developer can run the full stack locally with one command.
- Seeded demo data covers at least one SST company and one food quality company.
