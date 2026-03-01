# Quali Backend — Architecture & Naming Conventions

## Overview

Quali is a modular monolith built with **FastAPI + SQLModel + PostgreSQL**.
The architecture follows **Clean Architecture** principles inside each domain,
organised with **Domain-Driven Design** bounded contexts.

---

## Folder Structure

```
quali-backend/
├── main.py                        # Thin entrypoint — imports app from app/main.py
├── app/
│   ├── main.py                    # App factory: create_app(), register_routes/middlewares/errors
│   ├── domains/                   # Business bounded contexts
│   │   ├── certification/         # Reference domain (fully implemented)
│   │   ├── iam/
│   │   ├── education/
│   │   ├── compliance/
│   │   ├── quality_ops/
│   │   └── health/                # System health checks (no business logic)
│   ├── core/                      # Framework configuration (FastAPI concerns only)
│   │   ├── settings/              # Pydantic-settings per environment
│   │   ├── errors/                # Exception handler + mapper
│   │   ├── middlewares/           # Observability middleware
│   │   └── lifespans/             # Startup/shutdown (DB pool)
│   ├── shared/                    # Cross-domain utilities
│   │   ├── exceptions/            # Base domain exceptions
│   │   └── dependencies/          # Shared FastAPI Depends() providers
│   └── clients/                   # External service adapters
│       └── sql/                   # PostgreSQL async adapter
│           ├── ports/             # Protocol interfaces
│           └── adapters/          # Concrete implementations
```

---

## Domain Structure (Clean Architecture)

Every business domain follows this exact layout.
The `certification` domain is the canonical reference.

```
domains/{domain}/
├── domain/                        # Pure business logic — no framework imports
│   ├── entities/                  # Pydantic BaseModel value objects
│   ├── events/                    # Domain events (things that happened)
│   └── ports/                     # Repository interfaces (Protocol)
├── application/                   # Orchestration — coordinates domain + infrastructure
│   ├── use_cases/                 # One use case per action
│   └── services/                  # Optional: multi-use-case orchestration
├── infrastructure/                # Framework and DB details
│   ├── models/                    # SQLModel ORM models (table=True)
│   ├── repositories/              # Concrete DB implementations of ports
│   └── dependencies/              # FastAPI Depends() factories
└── presentation/                  # HTTP layer
    ├── routes/                    # Route handlers
    ├── schemas/                   # Request/response Pydantic models
    └── mappers/                   # Entity ↔ Schema converters
```

### Layer Dependency Rules

```
presentation → application → domain
infrastructure → domain (implements ports)
presentation → infrastructure (dependency injection only)
```

**Golden rule:** inner layers never import from outer layers.
`domain` knows nothing about FastAPI, SQLModel, or HTTP.

---

## Dependency Injection Flow

FastAPI resolves dependencies bottom-up at request time:

```
Route handler
  └── CreateCertificateUseCaseDependency
        └── build_create_certificate_use_case(repository)
              └── CertificateRepositoryDependency
                    └── build_certificate_repository(session)
                          └── PostgresSessionDependency
                                └── app.state.db.get_session()  ← pool
```

`app.state.db` is the `AsyncPostgresAdapter` created once at startup via lifespan.

---

## Naming Conventions

### Classes

| Layer | Suffix | Example |
|-------|--------|---------|
| Domain entity | `Entity` | `CertificateEntity` |
| Domain event | `Event` | `CertificateIssuedEvent` |
| Domain port | `Port` | `CertificateRepositoryPort` |
| ORM model | `Model` | `CertificateModel` |
| Repository | `Repository` | `CertificateRepository` |
| Use case | `UseCase` | `CreateCertificateUseCase` |
| Service | `Service` | `CertificateService` |
| Request schema | `RequestSchema` | `CreateCertificateRequestSchema` |
| Response schema | `ResponseSchema` | `CreateCertificateResponseSchema` |
| Mapper | `Mapper` | `CertificateMapper` |
| Exception | `Exception` | `CertificateNotFoundException` |
| Dependency alias | `Dependency` | `CreateCertificateUseCaseDependency` |

**Rationale:** suffixes make class purpose immediately clear in an LLM/agent context
without reading the file — `CertificateModel` vs `CertificateEntity` are unambiguous.

### Files

Files always use the same name as the class they contain, in `snake_case`:

| Class | File |
|-------|------|
| `CertificateEntity` | `certificate_entity.py` |
| `CertificateRepositoryPort` | `certificate_repository_port.py` |
| `CertificateModel` | `certificate_model.py` |
| `CreateCertificateUseCase` | `create_certificate_use_case.py` |
| `CreateCertificateRequestSchema` | `create_certificate_schema.py` |

Dependency factory files are prefixed with their verb:

| Function | File |
|----------|------|
| `build_certificate_repository` | `build_certificate_repository_dependency.py` |
| `build_create_certificate_use_case` | `build_create_certificate_use_case_dependency.py` |

### Functions

| Purpose | Verb | Example |
|---------|------|---------|
| Retrieve from existing source | `get_` | `get_postgres_session_dependency` |
| Construct a new instance | `build_` | `build_certificate_repository` |
| Route handler | `handle_` | `handle_create_certificate_route` |
| Registration helper | `register_` | `register_error_handlers` |

### Foldering Rule

**Always use folders, never flat files at a layer root.**

```
# WRONG
infrastructure/repositories.py

# CORRECT
infrastructure/repositories/certificate_repository.py
```

Every folder has an `__init__.py` that re-exports its public symbols.

---

## Settings

Resolved via `SCOPE` environment variable:

| `SCOPE` | Class | `DEBUG` |
|---------|-------|---------|
| `local` | `LocalSettings` | `True` |
| `test` | `TestSettings` | `True` |
| `prod` | `ProdSettings` | `False` |

`APP_NAME` and `API_PREFIX` are fixed across all environments (defined in `BaseAppSettings`).
`DEBUG`, `SCOPE`, `DATABASE_URL` have no base default — each env class sets its own value.

Local default: `DATABASE_URL = postgresql+asyncpg://quali:quali@localhost:5432/quali`

---

## Cross-Domain Communication — Contract Pattern

Domains must **never import from each other directly**. When one domain needs data
from another (e.g. `certification` looking up a `user`), it depends on a contract
defined in `app/shared/contracts/`.

### Structure

Each contract lives in its own folder with exactly two files:

```
app/shared/contracts/
├── __init__.py                              ← re-exports all ports + adapters
└── {verb}_{entity}/
    ├── {verb}_{entity}_port.py             ← Protocol + minimal result DTO (zero project imports)
    └── {verb}_{entity}_adapter.py          ← Adapter class + factory + Dependency alias
```

Example — `get_user_by_id`:

```
app/shared/contracts/get_user_by_id/
├── get_user_by_id_port.py      ← UserContractResult + GetUserByIdPort
└── get_user_by_id_adapter.py   ← GetUserByIdAdapter + build_* + GetUserByIdDependency
```

### Port file (pure — no framework imports)

```python
class UserContractResult(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str

class GetUserByIdPort(Protocol):
    async def __call__(self, user_id: str) -> UserContractResult | None: ...
```

### Adapter file (infrastructure — allowed to import domain internals)

```python
class GetUserByIdAdapter:
    def __init__(self, session: AsyncSession) -> None:
        self._repository = UserRepository(session=session)  # ← only crossing point

    async def __call__(self, user_id: str) -> UserContractResult | None:
        entity = await self._repository.get_by_id(user_id)
        if entity is None:
            return None
        return UserContractResult(id=entity.id, email=entity.email, ...)

def build_get_user_by_id_adapter(session: PostgresSessionDependency) -> GetUserByIdAdapter:
    return GetUserByIdAdapter(session=session)

GetUserByIdDependency = Annotated[GetUserByIdAdapter, Depends(build_get_user_by_id_adapter)]
```

### Consumer usage (e.g. certification use case)

```python
from app.shared.contracts import GetUserByIdPort, GetCompanyByIdPort

class CreateCertificateUseCase:
    def __init__(
        self,
        repository: CertificateRepositoryPort,
        get_user_by_id: GetUserByIdPort,       ← depends on the Protocol, not the adapter
        get_company_by_id: GetCompanyByIdPort,
    ) -> None: ...
```

The DI factory for the use case receives `GetUserByIdDependency` from `app/shared/contracts`.

### Dependency graph (no cycles possible)

```
app/domains/{any}/domain        → app/shared/contracts (port only)
app/shared/contracts/adapter    → app/domains/{source}/infrastructure (one crossing point)
app/domains/{any}/infrastructure/dependencies → app/shared/contracts (adapter + Dependency)
```

### Naming conventions

| File | Contains |
|---|---|
| `{verb}_{entity}_port.py` | `{Entity}ContractResult` (DTO) + `{Verb}{Entity}Port` (Protocol) |
| `{verb}_{entity}_adapter.py` | `{Verb}{Entity}Adapter` + `build_{verb}_{entity}_adapter` + `{Verb}{Entity}Dependency` |

---

## Entity Deletion — Tombstone Pattern

Domain tables are **never soft-deleted**. When an entity is deleted, the repository:

1. Fetches the ORM model from the DB.
2. Writes a `EntityTombstoneModel` snapshot to `entity_tombstones` (shared table).
3. Hard-deletes the original row.
4. Commits both operations atomically.

```
DELETE request
     │
     ▼
XxxRepository.delete()
     │
     ├── 1. session.get(XxxModel, id)
     ├── 2. EntityTombstoneModel(
     │         entity_type = "xxx",        ← polymorphic discriminator
     │         entity_id   = original ULID,
     │         payload     = full JSON snapshot,
     │         deleted_at  = datetime.now(UTC),
     │         deleted_by  = actor ULID,
     │       )
     ├── 3. session.add(tombstone)
     ├── 4. session.delete(model)
     └── 5. session.commit()              ← atomic — both or neither
```

**Benefits over soft-delete:**

| Concern | Soft-delete | Tombstone |
|---|---|---|
| Domain queries | Must always add `WHERE deleted_at IS NULL` | No filter needed — rows are gone |
| Domain models | Polluted with `deleted_at` column | Stay clean |
| Audit trail | Spread across all tables | Single `entity_tombstones` table |
| Schema evolution | Old snapshots break if columns change | JSON payload is immutable |

**Relevant files:**

```
app/shared/models/entity_tombstone_model.py   ← shared ORM model
app/domains/{domain}/
  infrastructure/repositories/{domain}_repository.py  ← delete() implementation
  application/use_cases/delete_{domain}_use_case.py   ← orchestrates the flow
```

---

## Exception Handling

```
app/shared/exceptions/
├── _domain_exception.py      # DomainException base (_prefix = don't use directly)
├── not_found_exception.py    # NotFoundException       → 404
├── conflict_exception.py     # ConflictException       → 409
├── unauthorized_exception.py # UnauthorizedException   → 401
├── forbidden_exception.py    # ForbiddenException      → 403
└── unprocessable_exception.py# UnprocessableException  → 422
```

Domain exceptions carry `error_code`, `message`, `context` — no HTTP knowledge.
HTTP mapping lives exclusively in `app/core/errors/error_mapper.py`.

**Subclass pattern for domain-specific errors:**

```python
# domains/certification/domain/exceptions/certificate_not_found_exception.py
class CertificateNotFoundException(NotFoundException):
    def __init__(self, certificate_id: str) -> None:
        super().__init__(
            message=f"Certificate '{certificate_id}' not found.",
            context={"certificate_id": certificate_id},
            error_code="CERTIFICATE_NOT_FOUND",
        )
```

Subclasses inherit the parent HTTP status code via MRO walk — no mapper registration needed.

---

## HTTP Response Shape

All error responses follow this structure:

```json
{
  "error_code": "CERTIFICATE_NOT_FOUND",
  "message": "Certificate '123' not found.",
  "context": { "certificate_id": "123" }
}
```

---

## Code Style

- **Imports:** absolute for cross-domain (`app.shared.exceptions`), relative for within-domain (max 3 dots)
- **Logging:** `%s` style inside `logger.*()` calls — lazy evaluation
- **f-strings:** everywhere else
- **Docstrings:** Google style on every file (module docstring) and every class/function
- **Formatter:** Ruff, line length 88
