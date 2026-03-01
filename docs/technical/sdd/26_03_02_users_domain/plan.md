# Users Domain + Company Members — Implementation Plan

## Overview
Implements the `users` domain and extends the `companies` domain with company membership.
Both are required prerequisites for the `certificates` domain.

## Part A — Users Domain (`app/domains/users/`)

### A1 — Domain Layer
- `domain/entities/user_entity.py` — `UserData` + `UserEntity(UserData, AuditEntity)`
- `domain/ports/user_repository_port.py` — `UserRepositoryPort(Protocol)`
- `domain/events/user_created_event.py` — `UserCreatedEvent(BaseModel)`

### A2 — Application Layer
| Use Case             | execute() signature              | Business logic                          |
|----------------------|----------------------------------|-----------------------------------------|
| CreateUserUseCase    | (data: UserData) → UserEntity    | email conflict check → save             |
| GetUserUseCase       | (user_id: str) → UserEntity      | get_by_id or NotFoundException          |
| UpdateUserUseCase    | (entity: UserEntity) → UserEntity| Pure save (Option B)                    |
| DeleteUserUseCase    | (user_id: str, deleted_by: str)  | get_by_id or NotFoundException → delete |

### A3 — Infrastructure Layer
- `infrastructure/models/user_model.py` — `UserModel(AuditModel, table=True)`
- `infrastructure/repositories/user_repository.py` — all queries filter `deleted_at IS NULL`
- `infrastructure/dependencies/` — one file per dependency factory

### A4 — Presentation Layer
- Schemas: `CreateUserRequestSchema`, `UpdateUserRequestSchema`, response schemas
- Mapper: `UserMapper.to_public_response()` / `UserMapper.to_private_response()`
- Routes: POST `/`, GET `/{id}`, PATCH `/{id}`, DELETE `/{id}`

## Part B — Company Members (extends `app/domains/companies/`)

### B1 — Domain Layer
- `domain/entities/company_member_entity.py` — `CompanyMemberData` + `CompanyMemberEntity`
- `domain/ports/company_member_repository_port.py` — `CompanyMemberRepositoryPort(Protocol)`

### B2 — Application Layer
| Use Case                   | execute() signature                                          |
|----------------------------|--------------------------------------------------------------|
| AddCompanyMemberUseCase    | (data: CompanyMemberData) → CompanyMemberEntity              |
| RemoveCompanyMemberUseCase | (company_id, user_id, deleted_by) → None                    |
| GetCompanyMembersUseCase   | (company_id: str) → list[CompanyMemberEntity]                |

### B3 — Infrastructure Layer
- `infrastructure/models/company_member_model.py` — no FK constraints
- `infrastructure/repositories/company_member_repository.py`
- `infrastructure/dependencies/` — four new dependency files

### B4 — Presentation Layer
- Schemas: `AddCompanyMemberRequestSchema`, `CompanyMemberResponseSchema`
- Mapper: `CompanyMemberMapper.to_response()`
- Routes: POST `/{id}/members`, GET `/{id}/members`, DELETE `/{id}/members/{user_id}`

## Migrations
1. `create_users_table` — users table with unique email index
2. `create_company_members_table` — company_members table with company_id and user_id indexes

## Tests
- `tests/users/` — FakeUserRepository + e2e + unit mapper tests
- `tests/companies/e2e/test_company_members.py` — add, list, remove, duplicate → 409
