# Naming Conventions

Every layer uses folders with individually named files.
No flat `entities.py`, `events.py`, or `service.py` — everything lives in a named folder
with a file per class. Every name must communicate its layer and purpose without
requiring the reader (human or LLM/agent) to open the file or inspect inheritance.

---

## Folder Structure per Domain

```
domains/{domain}/
├── domain/
│   ├── entities/
│   │   └── {entity}_entity.py
│   └── events/
│       └── {entity}_{past_action}_event.py
├── application/
│   ├── services/
│   │   └── {entity}_service.py
│   └── use_cases/
│       └── {action}_{entity}_use_case.py
├── infrastructure/
│   ├── models/
│   │   └── {entity}_model.py
│   └── repositories/
│       └── {entity}_repository.py
└── presentation/
    ├── routes/
    │   └── {action}_{entity}_route.py
    ├── schemas/
    │   └── {action}_{entity}_schema.py
    └── mappers/
        └── {entity}_mapper.py
```

---

## File and Class Naming

### `domain/entities/{entity}_entity.py`

Base: `pydantic.BaseModel`. Pure business object, zero framework dependencies.
One entity per file.

```
file:  certificate_entity.py
class: CertificateEntity
```

---

### `domain/events/{entity}_{past_action}_event.py`

Base: `pydantic.BaseModel`. One event per file. Name uses past tense action.

```
file:  certificate_issued_event.py
class: CertificateIssuedEvent

file:  certificate_revoked_event.py
class: CertificateRevokedEvent
```

---

### `infrastructure/models/{entity}_model.py`

Base: `SQLModel` with `table=True`. ORM representation only.
Never leaves the infrastructure layer.

```
file:  certificate_model.py
class: CertificateModel
```

---

### `infrastructure/repositories/{entity}_repository.py`

Plain class. Accepts and returns `Entity` objects — never exposes `Model` outside.

```
file:  certificate_repository.py
class: CertificateRepository
```

---

### `application/services/{entity}_service.py`

Plain class. Orchestrates use cases, manages transactions.

```
file:  certificate_service.py
class: CertificateService
```

---

### `application/use_cases/{action}_{entity}_use_case.py`

Plain class. One class per file, one responsibility per class.

```
file:  create_certificate_use_case.py
class: CreateCertificateUseCase

file:  revoke_certificate_use_case.py
class: RevokeCertificateUseCase

file:  verify_certificate_use_case.py
class: VerifyCertificateUseCase
```

---

### `presentation/schemas/{action}_{entity}_schema.py`

Base: `pydantic.BaseModel`. Two classes per file: request and response.

```
file:   create_certificate_schema.py
classes: CreateCertificateRequestSchema
         CreateCertificateResponseSchema
```

---

### `presentation/routes/{action}_{entity}_route.py`

Function, not a class.

```
file:     create_certificate_route.py
function: handle_create_certificate_route
```

---

### `presentation/mappers/{entity}_mapper.py`

Plain class with static methods. Converts `Entity` ↔ `Schema`. No business logic.

```
file:  certificate_mapper.py
class: CertificateMapper
```

---

## Summary Table

| Layer | Folder | File pattern | Class / function pattern |
|---|---|---|---|
| Domain | `domain/entities/` | `{entity}_entity.py` | `{Entity}Entity` |
| Domain | `domain/events/` | `{entity}_{past_action}_event.py` | `{Entity}{PastAction}Event` |
| Infrastructure | `infrastructure/models/` | `{entity}_model.py` | `{Entity}Model` |
| Infrastructure | `infrastructure/repositories/` | `{entity}_repository.py` | `{Entity}Repository` |
| Application | `application/services/` | `{entity}_service.py` | `{Entity}Service` |
| Application | `application/use_cases/` | `{action}_{entity}_use_case.py` | `{Action}{Entity}UseCase` |
| Presentation | `presentation/schemas/` | `{action}_{entity}_schema.py` | `{Action}{Entity}RequestSchema` / `{Action}{Entity}ResponseSchema` |
| Presentation | `presentation/routes/` | `{action}_{entity}_route.py` | `handle_{action}_{entity}_route` |
| Presentation | `presentation/mappers/` | `{entity}_mapper.py` | `{Entity}Mapper` |

---

## Rules

1. **Always folders, never flat files.** No `entities.py`, `events.py`, or `service.py` at layer root.
2. **One class per file.** Exception: schemas share a file (`RequestSchema` + `ResponseSchema`).
3. **No suffix = not accepted.** Every class name declares its layer.
4. **Repositories return entities, never models.**
5. **Services and use cases never touch schemas.** They receive and return `Entity` objects only.
6. **Mappers have no logic.** An `if` for business reasons belongs in the service or entity.
7. **Event names use past tense.** `CertificateIssuedEvent`, not `CertificateIssueEvent`.
8. **Route handlers are functions, not classes.** `handle_{action}_{entity}_route`.
