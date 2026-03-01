# Quali Backend — Enhancements Roadmap

Tracks strategic tooling and infrastructure improvements that are not
business features or bug fixes. Sourced from comparing the official
`fastapi/full-stack-fastapi-template` against our architecture.

---

## 1. Pre-commit hooks — P1 (do now)

**Why:** Enforce Ruff format/lint before every commit. Prevents noisy CI
failures and keeps the code style consistent without manual effort.

**Tasks:**
- [ ] Add `.pre-commit-config.yaml` with `ruff check --fix` and `ruff format`
- [ ] Run `uv run pre-commit install` in dev setup docs

---

## 2. GitHub Actions CI — P1 (before first external contributor)

**Why:** Auto-run linting, tests, and migration check on every PR.

**Tasks:**
- [ ] Add `.github/workflows/ci.yml`:
  - `ruff check` + `ruff format --check`
  - `uv run pytest`
  - `uv run alembic upgrade head` (against a test DB service)
- [ ] Add PostgreSQL service container to the workflow

---

## 3. Docker Compose — P1 (before staging deploy)

**Why:** Local dev parity — one command spins up Postgres + app + migrations.
Reference: `fastapi/full-stack-fastapi-template` `docker-compose.yml`.

**Tasks:**
- [ ] `docker-compose.yml` with services: `db`, `app`
- [ ] `Dockerfile` for the backend (multi-stage: build + runtime)
- [ ] Run migrations automatically on app startup (or as a separate service)
- [ ] `.env.example` documents all required vars

---

## 4. Mailcatcher — P2 (when email features land)

**Why:** Local email testing for password recovery and certificate delivery.
Catches outgoing emails in a web UI without a real SMTP server.

**Tasks:**
- [ ] Add `mailcatcher` service to `docker-compose.yml`
- [ ] Add `EMAIL_*` settings to `LocalSettings` pointing to Mailcatcher SMTP port
- [ ] Add an email client adapter in `app/clients/email/`

---

## 5. Traefik reverse proxy — P3 (production phase)

**Why:** Automatic HTTPS via Let's Encrypt, routing, load balancing.

**Tasks:**
- [ ] Add `docker-compose.prod.yml` with Traefik service
- [ ] Configure `traefik.toml` or labels for Let's Encrypt
- [ ] Document deployment flow in `docs/ops/`

---

## 6. Auto-generated API client — P3 (when frontend exists)

**Why:** The OpenAPI schema is already exposed by FastAPI. An auto-generated
TypeScript client removes manual maintenance of API contracts on the frontend.

**Tasks:**
- [ ] Evaluate `openapi-ts` or `hey-api` for client generation
- [ ] Add a `make generate-client` or `npm run generate` script
- [ ] Integrate into CI so the client is always in sync with the schema

---

## 7. Project scaffold template — Post-Quali (extract after Phase 2-3)

**Why:** Once `education` and `compliance` domains are done, the architecture
will have proven itself across 4+ domains. Extract a reusable scaffold so
future projects can start with this architecture via a single command.

**What to include:**
- `app/core/`, `app/shared/`, `app/clients/sql/` — framework skeleton
- `app/domains/health/` and `app/domains/iam/` — working auth out of the box
- One reference domain (`example/`) with full CRUD + auth guards to copy-paste
- `CLAUDE.md`, `ARCHITECTURE.md`, `.claude/commands/code_best_practices_skill.md`
- `pyproject.toml`, Ruff config, pre-commit hooks, GitHub Actions CI
- Copier or Cookiecutter templating for project name/author substitution

**When:** After Phase 2 (`education`) is complete. Patterns stabilize late —
do not extract early or the scaffold will reflect aspirational decisions.

**Target repo:** `fastapi-clean-ddd-template` (separate public repository)

---

## Suggested execution order

1. **#1** Pre-commit hooks — low effort, immediate quality gain
2. **#2** GitHub Actions CI — before second contributor joins
3. **#3** Docker Compose — before first staging environment
4. **#4** Mailcatcher — when email client is implemented
5. **#5** Traefik — production phase
6. **#6** Auto-generated client — when frontend work starts
7. **#7** Scaffold template — post Phase 2-3
