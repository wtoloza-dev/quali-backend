# Architecture Vision

## The Core Tension

Quali will eventually be a large distributed platform. But distributed systems have enormous operational cost — service discovery, network latency, distributed transactions, independent deployments, observability across services. Building a microservice architecture on day one for a product with zero users is one of the most common ways to kill a startup.

The goal is to write code today that does not block the architecture of tomorrow.

That discipline has a name: **Modular Monolith with DDD boundaries**.

---

## Three Horizons

### Horizon 1 — Today: Modular Monolith
*POC → MVP → first paying customers*

One codebase. One database. One deployment. But internally organized as if it will be split — because it will.

### Horizon 2 — Tomorrow: Selective Extraction
*Product-market fit achieved, load starts to diverge between domains*

Pull out the first service where extraction is clearly justified. The monolith becomes both the remaining application and the API gateway for the extracted service.

### Horizon 3 — Future: Distributed IMS Platform
*LATAM scale, multiple industries, external integrations*

Each domain is a service. The current FastAPI app is the API gateway. Education is a shared global platform. Everything else is per-tenant.

---

## The Key Insight: Separate Services per Domain, Not per Company

A common misread of multi-tenancy is "one server per company." That does not scale and is operationally catastrophic at 500 tenants.

The right separation is **per domain**:

| Service | Scope | Why separate |
|---|---|---|
| **Education** | Global — shared across ALL companies | Content is a marketplace, not per-tenant |
| **Certification** | Per-tenant | Certificates are private company records |
| **Compliance** | Per-tenant | Audits and CARs are sensitive company data |
| **Quality Ops** | Per-tenant | Incidents, NCMs, hazard matrices are internal |
| **Identity (IAM)** | Global — shared | Auth is the foundation for everything |

Education is genuinely different. A company does not need to build every course from scratch — they consume from a shared library, customize it, and the platform manages access. This is the Coursera/Udemy model, not the SharePoint model. A single education service with strong multi-tenant content permissions serves everyone.

---

## Horizon 1 — Modular Monolith in Detail

### Folder Structure (Domain-First, Not Layer-First)

The enemy of future extraction is organizing code by technical layer:
```
# BAD — extraction is impossible without touching everything
app/
  models/        ← all models mixed together
  schemas/       ← all schemas mixed together
  routers/       ← all routes mixed together
  services/      ← all business logic mixed together
```

The correct structure mirrors domain boundaries. Each domain is a vertical slice that owns its own models, logic, and API surface:

```
app/
  domains/
    iam/                      # Identity & Access Management
      models.py               # Company, User, Role
      schemas.py
      repository.py
      service.py
      router.py
      events.py               # Domain events emitted by this domain

    certification/            # Digital certificates + QR
      models.py               # Certificate, CertificateTemplate
      schemas.py
      repository.py
      service.py
      router.py
      events.py

    education/                # LMS — courses, enrollments, assessments
      models.py               # Course, Module, Lesson, Enrollment
      schemas.py
      repository.py
      service.py
      router.py
      events.py

    compliance/               # Standards, audits, CARs, documents
      models.py               # Standard, Audit, CorrectiveAction
      schemas.py
      repository.py
      service.py
      router.py
      events.py

    quality_ops/              # NCM, incidents, hazard matrix, HACCP
      models.py               # NonConformance, Incident, HazardMatrix
      schemas.py
      repository.py
      service.py
      router.py
      events.py

  shared/
    database.py               # SQLAlchemy session, engine
    auth.py                   # JWT decode, current_user dependency
    tenant.py                 # Tenant context middleware
    events.py                 # Domain event bus (in-process today)
    exceptions.py             # Shared exception types
    pagination.py

  main.py                     # App factory, router registration
```

### The Golden Rule of Domain Boundaries

> **A domain must never import from another domain's `models.py` or `repository.py`.**

If Domain A needs something from Domain B, it goes through Domain B's **service layer** — the same interface it would call over HTTP in Horizon 2. This convention costs nothing today and makes extraction trivial later.

```python
# WRONG — creates hard coupling, blocks extraction
from app.domains.education.models import Enrollment
from app.domains.education.repository import EnrollmentRepository

# CORRECT — talks through the service interface
from app.domains.education.service import EducationService

class CertificationService:
    def __init__(self, education_service: EducationService): ...
```

When Horizon 2 arrives and `EducationService` moves to a separate process, you replace the in-process call with an HTTP client — and nothing else changes.

### Domain Events (In-Process Today, Message Bus Tomorrow)

Cross-domain reactions (e.g., "when enrollment completes, issue a certificate") must not use direct service calls in both directions — that creates circular dependencies.

Instead, use **domain events**:

```python
# education/events.py
@dataclass
class EnrollmentCompleted:
    enrollment_id: UUID
    user_id: UUID
    course_id: UUID
    company_id: UUID
    score: int
    certificate_template_id: UUID | None

# education/service.py — emits the event
async def complete_enrollment(self, enrollment_id: UUID) -> None:
    # ... business logic ...
    await self.event_bus.publish(EnrollmentCompleted(...))

# certification/service.py — reacts to the event
async def on_enrollment_completed(self, event: EnrollmentCompleted) -> None:
    await self.issue_certificate(...)
```

In Horizon 1, `event_bus` is an in-process pub/sub (a simple dict of handlers). In Horizon 2, it becomes a message broker (Redis Streams or RabbitMQ). The business logic does not change.

### Database Strategy: One DB, Schema-Per-Domain

One PostgreSQL instance today. But each domain uses a dedicated schema:

```
postgres://
  quali/
    iam.companies
    iam.users
    iam.user_companies
    certification.certificates
    certification.templates
    education.courses
    education.enrollments
    compliance.standards
    compliance.audits
    quality_ops.non_conformances
    quality_ops.incidents
```

This enforces domain data ownership at the database level and makes the Horizon 2 migration surgical: move the `education.*` tables to a new database, update the connection string in the education domain, done.

**No cross-schema joins in application code.** If Certification needs an enrollment ID, it stores the ID as a plain `UUID` field — not a foreign key across schemas. Referential integrity within a domain is enforced by the DB. Cross-domain consistency is the application's responsibility.

---

## Horizon 2 — Extract Education First

### Why Education First

Education is the clearest extraction candidate because:

1. **It is genuinely global.** Course content is not per-tenant data. A company accesses the shared course library. This is fundamentally different from compliance audits or incidents.
2. **Read-heavy and cacheable.** Lesson content, course catalogs, and progress dashboards have very different load patterns from writing incident reports.
3. **Independent deployment cycle.** New course content, new question banks, new template libraries — these should deploy without touching the compliance or quality operations code.
4. **Zero circular dependencies.** Education emits events (`EnrollmentCompleted`). Other domains react. Education never calls back.

### What the Extraction Looks Like

```
Before Horizon 2:
  [Client] → [Quali API (monolith)] → [PostgreSQL]

After extracting Education:
  [Client] → [Quali API (gateway + remaining monolith)]
                    ├── /api/v1/education/* → HTTP → [Education Service] → [Education DB]
                    ├── /api/v1/certs/*     → (local)  [Certification domain]
                    ├── /api/v1/compliance/* → (local) [Compliance domain]
                    └── /api/v1/quality/*   → (local)  [Quality Ops domain]
```

The existing FastAPI app gains a transparent proxy layer for `/education/*` routes. From the client's perspective, the API surface does not change. JWT tokens are stateless — the education service validates them independently without calling home.

### Shared Auth in a Distributed Setup

JWT is the right choice here specifically because it is stateless. The education service does not need to ask the IAM service "is this token valid?" — it validates the signature locally using the shared public key. No network call. No shared session store.

```
IAM Service        →  issues JWT (signed with private key)
Education Service  →  validates JWT (using public key)
Certification      →  validates JWT (using public key)
Compliance         →  validates JWT (using public key)
```

The only thing services share is the public key — distributed as an environment variable or a well-known endpoint.

---

## Horizon 3 — Full Distributed IMS

```
                         ┌──────────────────────────────┐
                         │         API Gateway           │
                         │  (current FastAPI evolves)    │
                         │  routing / auth / rate limit  │
                         │  logging / tracing            │
                         └──────────┬───────────────────┘
                                    │
          ┌─────────────────────────┼──────────────────────────┐
          │                         │                          │
    ┌─────▼──────┐          ┌───────▼──────┐          ┌───────▼───────┐
    │    IAM     │          │  Education   │          │ Certification │
    │  Service   │          │   Service    │          │   Service     │
    │            │          │  (global,    │          │  (public QR   │
    │ companies  │          │  shared)     │          │  verification)│
    │ users/auth │          │              │          │               │
    └────────────┘          └──────────────┘          └───────────────┘

    ┌─────────────┐          ┌──────────────┐          ┌───────────────┐
    │ Compliance  │          │ Quality Ops  │          │ Notifications │
    │   Service   │          │   Service    │          │   Service     │
    │             │          │              │          │               │
    │ standards   │          │ incidents    │          │ email / push  │
    │ audits      │          │ NCM / HACCP  │          │ webhooks      │
    │ CARs        │          │ hazard matrix│          │               │
    └─────────────┘          └──────────────┘          └───────────────┘

                    ┌──────────────────────┐
                    │    Message Broker     │
                    │  (Redis Streams /     │
                    │   RabbitMQ)           │
                    │                       │
                    │  EnrollmentCompleted  │
                    │  CertificateIssued    │
                    │  IncidentReported     │
                    │  AuditCompleted       │
                    └──────────────────────┘
```

### What the API Gateway Does

The FastAPI app that starts as a monolith evolves into the gateway layer. It:
- Routes requests to the correct service.
- Validates JWT and injects tenant context before proxying.
- Enforces rate limiting per tenant.
- Aggregates responses for composite endpoints (e.g., dashboard that queries 3 services).
- Provides a single observability entry point (request ID, structured logging, tracing headers).
- Handles CORS, TLS termination, and API versioning in one place.

The gateway does not contain business logic. Business logic lives in services.

### Certification as a High-Performance Read Service

The public QR verification endpoint (`/verificar/<token>`) deserves special attention. At LATAM scale, this is the most frequently hit endpoint — anyone scanning a QR at a factory gate or Ministerio de Trabajo inspection hits it. It must:

- Return in < 200ms globally.
- Require no authentication.
- Be independently scalable.
- Be cacheable at the CDN level for valid certificates (immutable until revocation).

Extracting Certification as its own lightweight service allows it to be deployed on edge infrastructure and cached aggressively — independent of the operational complexity of the compliance or quality services.

---

## Decision Log

These are decisions that must be made correctly in Horizon 1 or they become expensive to change:

| Decision | Choice | Reason |
|---|---|---|
| Code organization | Domain-first folders | Enables extraction without restructuring |
| Cross-domain calls | Through service interfaces only | No coupling at model/repository level |
| Cross-domain reactions | Domain events | No circular dependencies, message-broker-ready |
| Database isolation | PostgreSQL schema per domain | One DB today, split cleanly tomorrow |
| Cross-domain references | UUID fields, no FK constraints | No cascades across schema boundaries |
| Auth mechanism | Stateless JWT | Works across services without shared session |
| API versioning | `/api/v1/` from day one | Gateway routing depends on stable path structure |
| Language for user-facing content | Spanish (es-CO) | Primary market; i18n keys from day one |

---

## What Stays Simple on Purpose

This architecture should not over-engineer Horizon 1. In the monolith phase:

- **No message broker.** The event bus is an in-process list of handlers. Redis or RabbitMQ is introduced only when the first service is extracted.
- **No service mesh.** Direct HTTP between the gateway and extracted services is sufficient until there are 4+ services.
- **No CQRS.** Read and write models are the same. Command/query separation is introduced per domain only when read performance becomes a real problem.
- **No GraphQL.** REST is simpler to reason about, easier to gateway, and sufficient for this domain.
- **One database.** Schema separation is enough. A database-per-service migration is a half-day task when the schemas are clean.

The complexity budget in Horizon 1 is spent on **getting the domain boundaries right**, not on infrastructure sophistication. A well-bounded modular monolith with clean domain events will outperform a poorly-bounded microservice architecture at every scale.
