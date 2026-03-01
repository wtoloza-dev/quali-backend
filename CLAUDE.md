# Quali Backend — Claude Instructions

Always follow the project best practices defined in `.claude/commands/code_best_practices_skill.md`.

Run `/code_best_practices_skill` mentally before starting any implementation task.

---

## Quick Reference (critical rules)

- **Architecture:** Clean Architecture + DDD modular monolith. Inner layers never import outer layers. `domain/` has zero framework imports.
- **IDs:** Always ULID as `str`. Never UUID.
- **Delete pattern:** Hard delete + tombstone. Before `session.delete(model)`, save a full JSON snapshot to `EntityTombstoneModel`. No `deleted_at` on domain tables. Never use `session.get()` for domain queries.
- **`updated_at`:** Never set in Python — DB manages it via `onupdate=text("now()")`.
- **Datetime:** `from datetime import UTC, datetime` → `datetime.now(UTC)`. Never `timezone.utc`.
- **Enums:** `StrEnum` in code, `sa.String()` in DB. One file per enum in `domain/enums/`. Never `sa.Enum()` or PG enum types.
- **Update use case:** Receives the full merged `XxxEntity` (Option B). No `UpdateData` class in the domain.
- **Slug:** Immutable — excluded from update schemas.
- **Tests:** `dependency_overrides` only. Never patch source code. `TestClient` (sync). `FakeRepository` in-memory.
- **Migrations:** Register models in `migrations/env.py`. Add `import sqlmodel` if the file uses `sqlmodel.sql.sqltypes.AutoString()`.
- **CLI:** Always `uv run` prefix (e.g. `uv run alembic upgrade head`, `uv run ruff check`).
- **Code style:** Double quotes, line length 88, Google-style docstrings on every module/class/function, Ruff formatter.

---

## Tech Stack

- **Framework:** FastAPI + SQLModel + SQLAlchemy (async) + PostgreSQL
- **Python:** 3.14+
- **Package manager:** `uv` (always prefix commands with `uv run`)
- **DB driver:** `asyncpg` (async), `psycopg2-binary` (Alembic sync)
- **Auth:** Firebase JWT verification (no service account) + ASGI middleware
- **IDs:** `python-ulid` (ULID as `str`)
- **Hashing:** `argon2-cffi`
- **Linter/formatter:** Ruff (line length 88, double quotes, Google docstrings)
- **Tests:** pytest + TestClient (sync) + testcontainers

---

## Architecture — Clean Architecture + DDD

### Layer dependency rules (NEVER violate)

```
presentation  →  application  →  domain
infrastructure  →  domain  (implements ports only)
presentation  →  infrastructure  (dependency injection only)
```

- `domain/` has **zero** framework imports (no FastAPI, SQLModel, SQLAlchemy)
- `application/` has **zero** HTTP knowledge
- ORM models never leave `infrastructure/`
- Repository concrete classes never leave `infrastructure/`

### Domain folder layout (mandatory for every domain)

```
domains/{domain}/
├── domain/
│   ├── entities/          # Pydantic BaseModel — input DTOs + full entities
│   ├── enums/             # StrEnum domain enums (one file per enum)
│   ├── events/            # Domain events
│   ├── exceptions/        # Domain-specific exceptions (extend DomainException)
│   ├── ports/             # Repository interfaces (Protocol)
│   └── value_objects/     # Immutable Pydantic models (frozen=True)
├── application/
│   ├── use_cases/         # One use case per action (single execute() method)
│   └── services/          # Multi-use-case orchestration (optional)
├── infrastructure/
│   ├── models/            # SQLModel ORM models (table=True)
│   ├── repositories/      # Concrete port implementations
│   └── dependencies/      # FastAPI Depends() factories
└── presentation/
    ├── routes/            # Route handlers
    ├── schemas/           # Request + response Pydantic models
    └── mappers/           # Entity ↔ Schema converters
```

**Foldering rule:** always use folders, never flat files at a layer root. Every folder has an `__init__.py` that re-exports its public symbols.

### Project structure overview

```
app/
├── main.py                    # FastAPI app factory & router registration
├── core/
│   ├── settings/              # Environment-based settings (local/test/prod)
│   ├── middlewares/            # AuthMiddleware (ASGI), CORS, Observability
│   ├── lifespans/             # Startup: AsyncPostgresAdapter; Shutdown: dispose
│   └── errors/                # DomainException → HTTP response mapping
├── clients/
│   └── sql/adapters/          # AsyncPostgresAdapter (pool + sessions)
├── shared/
│   ├── auth/                  # AuthContext, Role, dependencies, require_role
│   ├── contracts/             # Cross-domain port + adapter pattern
│   ├── dependencies/          # PostgresSessionDependency
│   ├── entities/              # AuditEntity base
│   ├── exceptions/            # DomainException + subclasses
│   ├── models/                # AuditModel, EntityTombstoneModel
│   ├── schemas/               # Shared Pydantic schemas
│   └── services/              # FirebaseAuthService, EncryptionService
└── domains/
    ├── health/                # System health checks
    ├── users/                 # User CRUD + self-registration
    ├── companies/             # Company/tenant + members + roles
    ├── iam/                   # JWT login + role assignment
    ├── certification/         # Certificate issuance + public verify
    ├── education/
    │   ├── courses/           # Courses + modules + lessons + access
    │   ├── enrollments/       # Enrollment lifecycle
    │   ├── assessments/       # Questions + attempts + scoring
    │   ├── access_codes/      # Access code generation & redemption
    │   └── training_plans/    # Training plan CRUD + items
    ├── compliance/            # Skeleton
    ├── quality_ops/           # Skeleton
    └── legal/                 # Infrastructure only (legal acceptance)
```

---

## Import Rules & Circular Import Prevention

### Golden rules

1. **Inner layers never import outer layers.** Domain never imports infrastructure or presentation.
2. **`__init__.py` under `app/shared/` must NEVER eagerly import modules that reach into `app/domains/*/infrastructure/`.** This is the pattern that causes circular imports.
3. **Cross-domain communication only through contracts** (`app/shared/contracts/`). Domain A never imports from Domain B's infrastructure.

### Known risk pattern (already mitigated)

`require_role` is intentionally **NOT re-exported** from `app/shared/auth/__init__.py` because it triggers:

```
auth/__init__ → require_role → contracts → adapter → repository → model → auth (CIRCULAR)
```

Import it directly: `from app.shared.auth.require_role import require_role`

### Prevention checklist for new code

- Adding a new re-export to a shared `__init__.py`? Trace the full import chain — if it reaches into `domains/*/infrastructure/`, do NOT add it.
- Adding a new contract adapter? It will import from a domain's infrastructure — make sure no `__init__.py` eagerly triggers it during model loading.
- Models importing shared enums? Import from the specific module file, never from a package that eagerly loads heavy dependencies.

---

## Request Lifecycle

1. **AuthMiddleware** (pure ASGI, soft-fail): extracts Bearer JWT → `FirebaseAuthService.decode()` → stores `AuthContext` in `ContextVar`
2. **Route handler** declares: `CurrentUserDependency` or `require_role(Role.X)`
3. **Dependency injection** resolves bottom-up: Route → Use Case → Repository → Session
4. **DB transaction**: auto-managed via `session.begin()` — repositories call `flush()`, never `commit()`
5. **On error**: transaction auto-rollbacks

---

## Auth & RBAC

### Auth context

- `AuthMiddleware` (ASGI) sets `ContextVar` from JWT. Soft-fail (no 401 at middleware level).
- `CurrentUserDependency = Annotated[AuthContext, Depends(get_current_user)]` — raises `UnauthorizedException` if no context.
- `OptionalCurrentUserDependency = Annotated[AuthContext | None, Depends(get_optional_current_user)]` — returns `None` if no context.
- Dev bypass: `x-dev-seed` header in local scope.

### Role hierarchy

```
VIEWER (10) < MEMBER (20) < ADMIN (30) < OWNER (40)
```

- Guard syntax: `auth: Annotated[AuthContext, require_role(Role.ADMIN)]`
- Lookup: queries `company_members` table for user's company role
- Higher roles pass lower guards (OWNER passes ADMIN guard)

### Tenant scoping

- `company_id` always comes from URL path param (AuthContext has no company_id)
- Cert get/revoke use `get_by_id_and_company`, never bare `get_by_id`
- DB constraints: `uq_company_members_company_user`, `uq_user_roles_user_company`

---

## Cross-Domain Contracts

Pattern for domain-to-domain communication without direct imports:

```
shared/contracts/{contract_name}/
├── {contract_name}_port.py       # Protocol interface + DTO
├── {contract_name}_adapter.py    # Concrete impl (imports ONE domain's infra) + Dependency
└── __init__.py                   # Re-exports
```

Available contracts: `get_user_by_id`, `get_company_by_id`, `get_company_member`, `list_certificates_by_recipient`, `save_legal_acceptance`

Usage in another domain:
```python
from app.shared.contracts import GetUserByIdDependency

async def handle_route(get_user: GetUserByIdDependency):
    user = await get_user(user_id=recipient_id)
```

---

## Naming Conventions

### Classes

| Layer | Suffix | Example |
|-------|--------|---------|
| Domain entity | `Entity` | `CompanyEntity` |
| Domain event | `Event` | `CompanyCreatedEvent` |
| Domain port | `Port` | `CompanyRepositoryPort` |
| ORM model | `Model` | `CompanyModel` |
| Repository | `Repository` | `CompanyRepository` |
| Use case | `UseCase` | `CreateCompanyUseCase` |
| Service | `Service` | `CompanyService` |
| Request schema | `RequestSchema` | `CreateCompanyRequestSchema` |
| Response schema | `ResponseSchema` | `CompanyPublicResponseSchema` |
| Mapper | `Mapper` | `CompanyMapper` |
| Exception | `Exception` | `CompanyNotFoundException` |
| Dependency alias | `Dependency` | `CreateCompanyUseCaseDependency` |

### Files — always `snake_case`, same name as the class inside

```
CompanyEntity         → company_entity.py
CompanyRepositoryPort → company_repository_port.py
CreateCompanyUseCase  → create_company_use_case.py
```

### Functions

| Purpose | Verb |
|---------|------|
| Retrieve from existing source | `get_` |
| Construct a new instance | `build_` |
| Route handler | `handle_` |
| Registration helper | `register_` |

---

## Entities — Two-Model Pattern

```python
class CompanyData(BaseModel):
    """Input fields — no audit columns."""
    name: str
    slug: str

class CompanyEntity(CompanyData, AuditEntity):
    """Full persisted entity. Inherits audit fields from AuditEntity."""
    pass
```

- `CompanyData`: use case input for **create**
- `CompanyEntity`: what every repository method returns
- **No `UpdateData` class** — presentation merges patch into full entity, passes `CompanyEntity` to `UpdateUseCase.execute(entity)`

---

## Enums — StrEnum + sa.String()

```python
# domain/enums/company_type.py
from enum import StrEnum

class CompanyType(StrEnum):
    PERSONAL = "personal"
    ORGANIZATION = "organization"
```

```python
# infrastructure/models/company_model.py
company_type: CompanyType = Field(sa_type=sa.String(), nullable=False)
```

- **Code handles validation** via StrEnum. **DB stores plain VARCHAR.**
- Never `sa.Enum()`, never PostgreSQL `CREATE TYPE`.
- One enum per file in `domain/enums/`.
- Migrations: enum columns use `sa.String()`, `server_default="value"` for defaults.

---

## Delete Pattern — Hard Delete + Tombstone

```python
tombstone = EntityTombstoneModel(
    entity_type="company",
    entity_id=model.id,
    payload={"id": model.id, ...},  # full JSON snapshot
    deleted_at=datetime.now(UTC),
    deleted_by=deleted_by,
)
self._session.add(tombstone)
await self._session.delete(model)
await self._session.flush()
```

- No `deleted_at` on domain tables. Deleted rows are gone.
- Never use `session.get()` for domain queries (bypasses select-based safety).

---

## Audit Fields

```python
# AuditModel (ORM)
id: str           # ULID primary key, default_factory=lambda: str(ULID())
created_at: datetime  # server_default=now()
created_by: str       # ULID of creator — always required, never hardcoded ""
updated_at: datetime  # server_default=now(), onupdate=text("now()") — NEVER set in Python
updated_by: str | None
```

- `created_by` always required on create use cases
- `updated_at` is **exclusively DB-managed**
- Self-registration: generate ULID in route, pass as both `user_id` and `created_by`

---

## Repository Pattern

```python
class CompanyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: CompanyEntity) -> CompanyEntity: ...
    async def get_by_id(self, company_id: str) -> CompanyEntity | None: ...
    async def update(self, entity: CompanyEntity) -> CompanyEntity: ...
    async def delete(self, company_id: str, deleted_by: str) -> None: ...

    @staticmethod
    def _to_entity(model: CompanyModel) -> CompanyEntity: ...
    @staticmethod
    def _to_model(entity: CompanyEntity) -> CompanyModel: ...
```

- `CompanyModel` never exposed outside the repository
- All public methods accept/return domain entities
- Repositories call `flush()`, never `commit()`

---

## Use Cases

```python
class CreateCompanyUseCase:
    def __init__(self, repository: CompanyRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, data: CompanyData) -> CompanyEntity: ...
```

- Constructor takes only ports (protocols), never concrete classes
- `execute()` is the only public method
- Raise domain exceptions (`NotFoundException`, `ConflictException`)

---

## Dependency Injection

```python
async def build_company_repository(
    session: PostgresSessionDependency,
) -> CompanyRepository:
    return CompanyRepository(session)

CompanyRepositoryDependency = Annotated[CompanyRepository, Depends(build_company_repository)]
```

- DI chain: route → use case → repository → session → DB pool
- Override at `build_{domain}_repository` level in tests

---

## HTTP Routes

```python
router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponseSchema)
async def handle_create_company_route(
    body: CreateCompanyRequestSchema,
    use_case: CreateCompanyUseCaseDependency,
) -> CompanyResponseSchema:
    entity = await use_case.execute(...)
    return CompanyMapper.to_response(entity)
```

- Handler name: `handle_{action}_{domain}_route`
- Status codes: 201 Create, 200 Get/Update, 204 Delete
- Routes registered in `app/main.py` under `/api/v1`

---

## Exceptions

```python
from app.shared.exceptions import NotFoundException

raise NotFoundException(
    message="Company not found.",
    context={"company_id": company_id},
    error_code="COMPANY_NOT_FOUND",
)
```

For domain-specific errors, subclass:
```python
class CompanyNotFoundException(NotFoundException):
    def __init__(self, company_id: str) -> None:
        super().__init__(
            message=f"Company '{company_id}' not found.",
            context={"company_id": company_id},
            error_code="COMPANY_NOT_FOUND",
        )
```

---

## Testing

### Structure
```
tests/{domain}/
├── conftest.py          # FakeRepository fixture
├── e2e/
│   ├── conftest.py      # TestClient + dependency_overrides
│   └── test_{action}_{domain}.py
└── unit/
    └── test_{domain}_mapper.py
```

### Rules
- **Never patch source code** — use `app.dependency_overrides` exclusively
- **FakeRepository** implements the domain `Port` protocol in-memory
- Override at `build_{domain}_repository` level
- Tests are **synchronous** — use `TestClient` (not `AsyncClient`)
- Set `SCOPE=test` in `tests/conftest.py` before any app imports
- Reset `dependency_overrides` after each test (`yield` fixture + teardown)
- Auth override: `get_current_user` → fake AuthContext
- `FakeUserRoleRepository.save()` must be present — used by OWNER bootstrap

---

## Alembic Migrations

- **Generate:** `make migration m="description"` (or `uv run alembic revision --autogenerate -m "..."`)
- **Apply:** `make migrate` (or `uv run alembic upgrade head`)
- **Register** every new Model in `migrations/env.py` with `import app.domains.{domain}.infrastructure.models`
- Model's `__init__.py` must import the class for SQLModel metadata registration
- Add `import sqlmodel` to migration if it uses `sqlmodel.sql.sqltypes.AutoString()`
- Enum columns: always `sa.String()`, never `sa.Enum()`
- `updated_at`: always `server_default=sa.func.now()` + `onupdate=text("now()")`

---

## CLI Commands

```bash
make dev              # Run FastAPI dev server
make db               # Start Docker PostgreSQL
make migrate          # Run all migrations
make migration m="x"  # Create new migration
make stop             # Kill server + stop DB
make down             # Full shutdown (server + DB + Colima)
```

All commands use `uv run` prefix. Never call python directly.

---

## Code Style

- **Double quotes** everywhere
- **Line length:** 88
- **Docstrings:** Google style on every module, class, and public function
- **Imports:** absolute for cross-domain (`app.shared.exceptions`), relative within domain (max 3 dots)
- **Logging:** `%s` style inside `logger.*()` — lazy evaluation
- **f-strings:** everywhere else
- **Linter:** `uv run ruff check`
- **Formatter:** `uv run ruff format`
