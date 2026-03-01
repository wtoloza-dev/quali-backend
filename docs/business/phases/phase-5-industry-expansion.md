# Phase 5 — Industry Vertical Expansion

## Goal

Extend Quali beyond the two initial verticals (SST and food quality) to serve additional Colombian industries that operate under their own regulatory frameworks. The core platform infrastructure built in Phases 0–4 does not change — new verticals are enabled through the standards library, role configuration, and specialized module extensions.

This phase validates that the "standards as data" architectural decision made in Phase 0 actually works at scale. Each new vertical is largely a data and configuration effort, with targeted feature additions only where the industry's workflow is genuinely different.

---

## Why Expand Now

By Phase 5, Quali has proven product-market fit in the SST and food quality segments. Companies using the platform for both verticals are naturally asking: "Can we also manage our ISO 9001 quality system here?" or "We have a construction division — can Quali handle their SG-SST too?"

The expansion is pull-driven. The platform is already capable of serving these industries structurally — Phase 5 adds the domain-specific standards, checklist templates, and workflow extensions each vertical requires.

---

## Target Verticals

### Vertical 3 — General Quality Management (ISO 9001)

**Who needs this:** Any Colombian manufacturing, service, or logistics company seeking or maintaining ISO 9001 certification — the world's most widely adopted quality standard.

**What already works (from Phases 0–4):**
- Standards library (ISO 9001 clauses pre-loaded)
- Compliance gap assessment
- Audit management
- Document control
- Corrective action workflow
- KPI dashboard

**New additions for ISO 9001:**
- Customer satisfaction management: surveys, complaint tracking, satisfaction score trends.
- Design and development control (clause 8.3): project-based product/service design records with review stages and approvals.
- Service delivery quality: define service specifications and record delivery conformance.
- Management review agenda template and record keeping (clause 9.3).
- Context of the organization: stakeholder register, SWOT/PESTLE analysis (clause 4).
- Risk and opportunity register (clause 6.1) — distinct from SST hazard matrix.

**Regulatory references:**
- ISO 9001:2015 (NTC ISO 9001 Colombian adoption)
- ICONTEC certification requirements

---

### Vertical 4 — Construction Safety

**Who needs this:** Colombian construction companies — one of the highest-risk sectors under Res. 0312 (classified as risk level IV, the highest). Governed by the same SG-SST framework as Vertical 1 but with construction-specific requirements.

**What already works:**
- SG-SST compliance assessment
- Hazard matrix (GTC 45)
- Incident and accident management
- SST training and induction certificates
- COPASST inspections

**New additions for construction:**

- **Permisos de trabajo (work permits):** Formal hot work, confined space entry, work at height, and electrical work permits. Each permit has a checklist, authorization chain, and validity window. Workers must hold the relevant certificate (Phase 1) to be authorized.
- **Site-level SG-SST:** Construction projects have separate SST management per site. A company manages multiple active sites simultaneously, each with its own hazard matrix, inspector, and incident log.
- **Subcontractor SST qualification:** Construction companies use many subcontractors. Each must demonstrate a valid SG-SST before being allowed on site — similar to supplier qualification in food quality but for safety compliance.
- **Pre-task safety analysis (AST — Análisis de Seguridad en el Trabajo):** Daily or per-task safety analysis completed by the work team before starting a high-risk activity. Mobile-first form.
- **Scaffolding and equipment inspection logs:** Periodic inspection records for scaffolding, cranes, hoists, and heavy equipment.

**Regulatory references:**
- Res. 0312 — Risk Level IV requirements
- Res. 1409 de 2012 — Work at height regulation
- Res. 0491 de 2020 — Confined space safety
- NTC 2561 — Safety in construction

---

### Vertical 5 — Healthcare Quality & Safety

**Who needs this:** Clinics, hospitals, laboratories, and healthcare service providers in Colombia. Subject to both SST requirements (biological risk is extremely high) and healthcare quality standards from the Supersalud and the Ministerio de Salud.

**What already works:**
- SG-SST compliance (biological hazard classification in GTC 45)
- Training and certification
- Document control
- Audit management

**New additions for healthcare:**

- **Biosafety protocols:** Structured management of biological risk protocols — standard precautions, PPE for biological exposure, waste management (residuos peligrosos hospitalarios).
- **Healthcare quality standards:** ICONTEC NTC-ISO 9001 applied to health services, Resolution 3100 de 2019 (habilitación de servicios de salud).
- **Pharmacovigilance and hemovigilance:** Adverse event reporting for medications and blood products.
- **Patient safety incidents:** Near-miss and adverse event reporting adapted for clinical settings (distinct from occupational incidents).
- **Critical equipment management:** Biomedical equipment calibration and maintenance records.

**Regulatory references:**
- Res. 0312 — Biological risk classification
- Res. 3100 de 2019 — Healthcare service enabling (habilitación)
- Decreto 351 de 2014 — Hospital waste management
- NTS-USNA (tourism and food service quality norms for hospital catering)

---

### Vertical 6 — Agriculture & Agribusiness

**Who needs this:** Colombian agricultural producers, flower exporters, coffee cooperatives, and agribusiness companies — a major economic sector with increasing pressure from international buyers requiring food safety and traceability certifications.

**What already works:**
- Food quality compliance (ISO 22000, HACCP)
- SST compliance (agricultural work is risk level III–IV)
- Training and certification
- Supplier management

**New additions for agriculture:**

- **GlobalG.A.P. compliance:** A major international certification required by European supermarkets for fresh produce exporters. Pre-loaded checklist covering: food safety, environmental sustainability, worker welfare, traceability.
- **Pesticide application records:** Log pesticide applications by plot — product, dose, operator, application date, re-entry interval, pre-harvest interval. Mandatory for export certificates.
- **Plot/field management:** Geographic register of production plots with associated crop, current cycle, and applied treatments.
- **Water quality monitoring:** Irrigation water testing records linked to HACCP water safety requirements.
- **Worker welfare (labor standards):** Housing, working hours, and wellbeing records required by GlobalG.A.P. and Rainforest Alliance certifications.
- **Chain of custody:** From plot to export — linking harvest lot to pesticide records, to packing, to export certificate.

**Regulatory references:**
- ICA (Instituto Colombiano Agropecuario) regulations
- INVIMA for processed agricultural products
- GlobalG.A.P. IFA standard
- Rainforest Alliance 2020 standard

---

## What Phase 5 Does Not Change

- **Core data model**: no new models for multi-tenancy, auth, or auditing — these are already generic.
- **Certification and LMS**: Phase 1 and 2 serve all new verticals without modification. New course templates and certificate types are added as data.
- **Compliance and CAR workflow**: Phase 3 works for all verticals — new standards are loaded into the library.
- **Incident and NCM management**: Phase 4's generic non-conformance model handles all verticals. New source types and categories are configuration.

**What is genuinely new per vertical:**
- Work permit module (construction)
- Site-level management (construction)
- Subcontractor SST qualification (construction)
- Pre-task analysis (construction)
- Biosafety protocols (healthcare)
- Pesticide application records (agriculture)
- Plot/field management (agriculture)
- GlobalG.A.P. compliance module (agriculture)

---

## Rollout Strategy

New verticals are not launched simultaneously. Each vertical is launched as a controlled expansion based on market demand signals:

1. **ISO 9001** — First, because it reuses 100% of existing infrastructure. The product difference is configuration and templates, not features.
2. **Construction** — High demand (largest worker population in Colombia), high SST regulatory pressure, work permit module is the key differentiator.
3. **Agriculture** — Strong export-driven demand for GlobalG.A.P., large market in coffee, flowers, and fresh produce.
4. **Healthcare** — Most complex, most regulated, requires dedicated compliance validation with healthcare regulatory experts.

---

## Success Criteria

- An ISO 9001 company can run a full gap assessment, manage CARs, and generate a management review record without any food or SST content appearing in their workspace.
- A construction company can issue work-at-height permits, manage multiple active sites, and qualify subcontractors for SST compliance.
- An agricultural exporter can maintain pesticide application records, link them to harvest lots, and generate a GlobalG.A.P. evidence summary.
- Adding a new vertical for a new customer requires no code deployment — only data configuration.
