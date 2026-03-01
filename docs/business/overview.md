# Quali — Platform Overview

## Vision

Quali is a B2B SaaS platform built for food industries that need to manage, certify, and continuously improve their quality systems.

The long-term goal is a unified platform covering the full quality lifecycle: training people, issuing verifiable credentials, managing compliance with ISO standards (ISO 22000, ISO 9001, HACCP), and orchestrating quality processes across the organization using BPM best practices.

---

## The Problem

Food companies operate under strict regulatory pressure. They must:

- Train and certify their workforce continuously.
- Maintain audit-ready evidence of compliance.
- Manage non-conformances, corrective actions, and supplier quality.
- Keep up with ISO standard updates and internal process changes.

Today most companies handle this with spreadsheets, disconnected LMS tools, paper-based audits, and manual certificate tracking. That creates risk, duplication, and blind spots.

---

## The Solution

Quali replaces that fragmented stack with a single platform organized around four concerns:

| Layer | What it does |
|---|---|
| **People** | Train, assess, and certify workforce |
| **Credentials** | Issue tamper-proof certificates, validate them in real time |
| **Compliance** | Map the company against ISO standards, track gaps and audits |
| **Operations** | Manage the living quality system — processes, incidents, suppliers |

---

## Approach Challenge & Notes

> These are architectural and product decisions worth debating before each phase begins.

### On Phase ordering

Your original ordering (Certify → Educate → Manage) is counterintuitive at first — you normally educate before certifying. However it is a **valid product strategy**:

- Certificate validation is a small, shippable MVP that builds trust and gets companies onboarded early.
- It creates a pull toward the education platform: "where do I get trained to earn this certificate?"
- It validates demand before investing in heavy content infrastructure.

The risk is that Phase 1 certificates without Phase 2 have no learning path attached, so they feel like orphan credentials. This can be mitigated by designing Phase 1 data models to already accommodate future course linkage.

### On multi-tenancy

This must be a first-class decision made in Phase 0, not retrofitted later. Every company using Quali is a `tenant`. Every resource — users, certificates, courses, audits — must be scoped to a tenant from day one. Skipping this will force a painful migration later.

### On Phase 3 scope

"Business management for the quality system" is enormous. ISO 22000 alone covers food safety management, hazard analysis, prerequisite programs, traceability, and more. Phase 3 needs to be split into at least two phases — Compliance & Audits first, then full QMS operations.

### On future integrations

Food companies use ERP systems (SAP, Oracle, TOTVS). A future integration layer will be necessary. Keep API contracts clean from Phase 1.

---

## Platform Phases

| Phase | Name | Status |
|---|---|---|
| 0 | Foundation | Planned |
| 1 | Digital Certification | Planned |
| 2 | Education Platform | Planned |
| 3 | Compliance & Audits | Planned |
| 4 | Full Quality Management System | Planned |

See [`phases/`](./phases/) for detailed breakdowns.

---

## Target Users

- **Quality Managers** — own the compliance and audit process.
- **Training Coordinators** — manage courses, enrollments, and certification tracking.
- **Operators / Line Workers** — take courses, receive certificates.
- **Auditors** — internal or external, reviewing evidence and gaps.
- **Company Admins** — manage users, roles, and company settings.

---

## Tech Stack (Backend)

- **Runtime**: Python 3.14
- **Framework**: FastAPI
- **Package manager**: uv
- **Linting / Formatting**: Ruff
