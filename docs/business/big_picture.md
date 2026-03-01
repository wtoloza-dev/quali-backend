# Quali — Big Picture

## The Shift in Vision

Originally scoped as a food quality platform, Quali is better understood from day one as a **multi-standard Integrated Management System (IMS) platform for Colombian and LATAM industries.**

Food quality and occupational safety are the two entry verticals — not because the platform is limited to them, but because they represent the highest regulatory pressure and the largest underserved market in Colombia right now.

The architecture must reflect this from the first line of code. Standards are data, not hardcoded logic. Industries are configuration, not separate products.

---

## Why Colombia First

### SG-SST is Mandatory for Every Colombian Company

The **Sistema de Gestión de Seguridad y Salud en el Trabajo (SG-SST)**, regulated by **Decreto 1072 de 2015** and **Resolución 0312 de 2019**, is not optional. Every company operating in Colombia — regardless of size or industry — is legally required to implement and maintain an occupational health and safety management system.

This is Quali's largest immediate market signal:

- Built-in demand. The law creates it.
- Most companies, especially SMEs, manage their SG-SST in spreadsheets, Word documents, or through their ARL's (Administradora de Riesgos Laborales) basic tools — which are generic, disconnected, and not audit-ready.
- Non-compliance carries fines and work suspension orders from the **Ministerio de Trabajo**.

This alone justifies building the platform with occupational safety as a first-class vertical alongside food.

### Food Quality Regulation in Colombia

- **INVIMA** (Instituto Nacional de Vigilancia de Medicamentos y Alimentos) regulates food safety.
- **Resolución 2674 de 2013** mandates Buenas Prácticas de Manufactura (BPM/GMP) for food handling companies.
- ISO 22000 and HACCP adoption is growing, especially in mid-to-large food producers and exporters.
- Food companies that export to the US or EU face FSMA and EU food law compliance on top of local requirements.

### The Colombian SME Gap

Large Colombian companies already use enterprise tools (SAP QM, ISOTools, Isolución). The underserved segment is the **growing Colombian SME** — 50 to 500 employees — that:

- Is subject to the same regulatory requirements as large companies.
- Cannot afford or implement enterprise-grade software.
- Lacks dedicated quality or safety staff, so whoever manages compliance does it part-time.
- Needs something opinionated, affordable, and in Spanish with local regulatory context baked in.

That is Quali's initial target customer.

---

## Two Entry Verticals

### Vertical 1 — Occupational Health & Safety (SST)

**Colombian regulatory framework:**
- Decreto 1072 de 2015 — Comprehensive labor regulations
- Resolución 0312 de 2019 — Minimum SST standards by company size
- ISO 45001:2018 — International OHS management standard (aligned with SG-SST structure)

**Key processes to support:**
- Risk identification and hazard matrix (Matriz de Peligros y Valoración de Riesgos)
- Accident and incident reporting and investigation
- Occupational health surveillance programs (PVVS)
- Personal protective equipment (EPP) control
- Emergency plans and drills
- SST training and inductions (with certificates)
- ARL coordination and reporting
- Annual SST management review

**Who manages this:**
- SST Coordinator or HSEQ Manager
- Every company with 10+ employees must have a COPASST (Comité Paritario de SST)
- Companies with 50+ employees need a dedicated SST professional

---

### Vertical 2 — Food Quality & Safety

**Colombian regulatory framework:**
- Resolución 2674 de 2013 — BPM for food establishments
- Decreto 1500 de 2007 — Meat and meat products
- INVIMA inspections and sanitary certificates (Concepto Sanitario)
- ISO 22000:2018 — Food safety management
- FSSC 22000 — For exporters

**Key processes to support:**
- BPM / GMP compliance assessment
- HACCP plan management (hazard analysis, CCPs, limits)
- Supplier qualification and raw material control
- Sanitary inspection readiness
- Product traceability
- Food safety training and handler certification
- Non-conformance and product recall management

**Who manages this:**
- Quality Director / Food Safety Manager
- Production supervisors
- Regulatory affairs team (for exporters)

---

## Platform Architecture Principle: Standards as Data

The single most important architectural decision for multi-industry support is that **no standard is hardcoded in application logic.**

```
Standard (data)
  ├── ISO 45001 clauses
  ├── SG-SST / Resolución 0312 requirements
  ├── ISO 22000 clauses
  ├── BPM / Resolución 2674 requirements
  ├── ISO 9001 clauses
  └── [any future standard]
```

Every compliance assessment, audit checklist, gap report, and corrective action workflow operates against this generic structure. Adding a new standard or a new country's regulatory framework is a data import — not a development sprint.

---

## Industries Quali Can Serve (Current Architecture)

| Industry | Standards / Regulations | Initial Focus |
|---|---|---|
| Food & Beverage | ISO 22000, HACCP, BPM, INVIMA | Yes — Vertical 2 |
| Manufacturing | SG-SST, ISO 45001, ISO 9001 | Yes — Vertical 1 |
| Construction | SG-SST, high-risk activities (Res. 0312 risk level IV) | Phase 5+ |
| Healthcare | SG-SST, ISO 9001, ICONTEC standards | Phase 5+ |
| Agriculture | SG-SST, food safety at origin, pesticide control | Phase 5+ |
| Logistics & Cold Chain | SG-SST, ISO 22000 (transport), BPM | Phase 5+ |
| Mining | SG-SST, risk level IV, environmental | Phase 5+ |

---

## LATAM Expansion Map

The regulatory frameworks across LATAM share structural similarities — most countries have adopted ISO standards locally and have mandatory occupational safety laws modeled after ILO conventions. This makes expansion a matter of localizing the standards library and adjusting regulatory references.

| Country | OHS Framework | Food Safety Framework |
|---|---|---|
| **Colombia** | SG-SST / Decreto 1072 / Res. 0312 | INVIMA / Res. 2674 / ISO 22000 |
| **México** | STPS / NOM-035 / NOM-030 | COFEPRIS / NOM-251 / FSMA (exporters) |
| **Perú** | Ley 29783 / DS 005-2012 | SENASA / DIGESA / ISO 22000 |
| **Chile** | Ley 16.744 / DS 40 / ISO 45001 | SAG / SEREMI / ISO 22000 |
| **Argentina** | SRT / Ley 24.557 / Res. SRT | SENASA / ANMAT / ISO 22000 |
| **Brasil** | NRs (NR-1 a NR-38) / eSocial | ANVISA / RDC 275 / ISO 22000 |

**Expansion sequencing logic:**
1. Colombia — build, validate, achieve product-market fit.
2. México or Chile — similar regulatory culture, large SME market, early adopters of ISO frameworks.
3. Rest of LATAM — with a localized standards library system, entry cost per country drops significantly.

---

## Revised Platform Vision Statement

> Quali is an Integrated Management System platform for Colombian and LATAM industries. It unifies occupational safety, food quality, and quality management into a single system — replacing disconnected spreadsheets, generic ARL tools, and expensive enterprise software with something modern, affordable, and built for the regulatory reality of the region.

---

## What This Means for Development

### Immediate implications (before writing a single route):

1. **No food-only data models.** Every model that could apply to SST must be designed generically. `Certificate` is not a "food certificate" — it is a certificate. `Course` is not a "food safety course" — it is a course. Industry context comes from tags and standard linkage.

2. **Language is Spanish first.** Error messages, email templates, PDF exports, and UI copy are in Spanish. English is secondary. The regulatory vocabulary (SG-SST, COPASST, PVVS, BPM, HACCP) must be native to the system.

3. **Tenant configuration includes industry vertical.** When a company is onboarded, they select their applicable standards. This drives what appears in their dashboard, what checklists are available, and what reports are generated.

4. **Colombian regulatory calendar is a feature.** Resolución 0312 has specific annual deliverables by company size. The platform should know these deadlines and surface them proactively.

---

## Updated Phase Overview

| Phase | Name | What changes with multi-industry scope |
|---|---|---|
| 0 | Foundation | Multi-tenancy + industry vertical configuration at tenant setup |
| 1 | Digital Certification | Generic certificates — SST induction certs, food handler certs, any cert |
| 2 | Education Platform | Courses for SST (COPASST, inductions, EPP) and food safety (HACCP, BPM) |
| 3 | Compliance & Audits | Standards library includes SG-SST/Res. 0312 and ISO 22000/BPM from day one |
| 4 | Full QMS | NCM for both safety incidents and food non-conformances; unified dashboard |
| 5 | Industry Expansion | Construction, healthcare, agriculture verticals |
| 6 | LATAM Localization | Country-specific standard libraries, language packs, regulatory calendars |
