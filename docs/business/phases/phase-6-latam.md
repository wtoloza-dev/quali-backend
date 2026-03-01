# Phase 6 — LATAM Expansion

## Goal

Scale Quali beyond Colombia into the broader LATAM market — starting with México and Chile, then progressively covering Peru, Argentina, and Brazil. The expansion strategy is built on the "standards as data" principle: each country's regulatory framework is modeled as a standards library extension, not a codebase fork.

This phase is as much a business and operational challenge as a technical one. Regulatory localization, local partnerships, language variants, and go-to-market strategy are as critical as any feature shipped.

---

## Why LATAM is a Natural Expansion

### Shared Structural Foundations

Most LATAM countries share:
- A mandatory occupational safety law modeled after ILO Convention 155.
- A national food safety regulatory body with BPM/GMP requirements.
- ISO 9001/ISO 22000/ISO 45001 adoption growing in the mid-market.
- Large SME sectors underserved by expensive enterprise software.
- Spanish as the working language (except Brazil).

This means the platform's core logic, UX vocabulary, and training content translate with minimal effort. The main localization work is:

1. Mapping the country's specific standards into the standards library.
2. Adapting legal forms and report templates (e.g., FURAT equivalent in each country).
3. Configuring country-specific regulatory calendars.
4. Establishing local legal and billing entities.

### The SME Gap Exists Across the Region

The same pattern found in Colombia repeats across LATAM: enterprise tools (SAP QM, ISOTools, Intelix) serve the top 5% of companies. The other 95% — 50 to 500 employees — use spreadsheets and generic tools. Quali's positioning is identical in every target country.

---

## Expansion Sequencing

### Priority 1 — México

**Why México first:**
- Largest economy in LATAM after Brazil.
- Strong manufacturing base (automotive, food, aerospace) with high ISO adoption.
- NOM-035 (psychosocial risk management) has created urgency similar to Colombia's SG-SST — it is mandatory for all companies.
- COFEPRIS (food and drug regulator) requirements align closely with INVIMA.
- Large Colombian diaspora in business circles — natural referral network.

**Key regulatory additions:**

| Standard | Domain | Colombian equivalent |
|---|---|---|
| NOM-030-STPS-2009 | Occupational safety management | SG-SST / Decreto 1072 |
| NOM-035-STPS-2018 | Psychosocial risk | (no direct equivalent) |
| NOM-019-STPS-2011 | Safety commissions | COPASST equivalent |
| NOM-251-SSA1-2009 | BPM for food | Res. 2674 |
| NOM-251 + COFEPRIS regs | Food safety | INVIMA framework |

**New feature: Psychosocial Risk Assessment (NOM-035)**
This is México-specific and has no Colombian equivalent. NOM-035 requires companies to apply a validated questionnaire to identify and prevent psychosocial risk factors and traumatic events. It is mandatory for companies with 16+ employees (phase II) or 50+ employees (phase III).

The platform needs:
- Validated NOM-035 questionnaire (Guía de referencia II — 72 items for 50+ employees).
- Anonymous response collection with statistical analysis.
- Category scoring: organizational environment, work factors, labor relationships.
- Action plan requirement for companies scoring above threshold.
- Evidence report for STPS inspection.

---

### Priority 2 — Chile

**Why Chile:**
- Most advanced regulatory environment in South America — ISO adoption is highest in the region.
- Mutual insurance system (ACHS, IST, Mutual de Seguridad) similar in structure to Colombian ARLs.
- NTP-ISO 45001 has been widely adopted alongside Ley 16.744.
- Strong agribusiness and food export sector (wine, salmon, fresh produce) with high GlobalG.A.P. and ISO 22000 demand.

**Key regulatory additions:**

| Standard | Domain | Colombian equivalent |
|---|---|---|
| Ley 16.744 | Occupational accident insurance | SG-SST base law |
| DS 40 | Occupational diseases | Enfermedad laboral classification |
| DS 594 | Basic sanitary and environmental conditions | BPM/workplace conditions |
| DS 76 | Construction safety | Res. 0312 risk level IV |
| SAG + SEREMI regs | Food safety | INVIMA + Res. 2674 |

**New feature: Mutual Insurance (Mutualidades) Integration**
Chilean companies report AT to one of three mutualidades (ACHS, IST, Mutual de Seguridad). The platform needs to generate the DIAT (Denuncia Individual de Accidente del Trabajo) form in the format expected by the respective mutual — the Chilean equivalent of the FURAT.

---

### Priority 3 — Perú

**Key regulatory additions:**

| Standard | Domain |
|---|---|
| Ley 29783 + DS 005-2012 | Occupational Safety and Health |
| DS 007-98-SA | Food safety and hygiene |
| NTP-ISO 45001 | OHS management |
| DIGESA regulations | Food safety regulator |
| SENASA | Agricultural safety |

**Distinctive feature: IPER (Identificación de Peligros y Evaluación de Riesgos)**
Peru's occupational safety law requires the IPER methodology — structurally similar to GTC 45 but with a different matrix format and risk categorization. A Peru-specific risk matrix template is needed alongside the existing GTC 45 implementation.

---

### Priority 4 — Argentina

**Key regulatory additions:**

| Standard | Domain |
|---|---|
| Ley 19.587 + Decreto 351/79 | Occupational health and safety |
| Ley 24.557 | Occupational risk insurance (ART) |
| Resoluciones SRT | Specific OHS requirements |
| CAA (Código Alimentario Argentino) | Food safety |
| SENASA | Agrifood safety |

**Distinctive feature: ART (Aseguradoras de Riesgos del Trabajo)**
Argentina's worker compensation system uses ARTs (similar to ARLs in Colombia). Incident reporting (Denuncia de Accidente) goes to the ART. The platform needs Argentine-specific incident report generation compatible with ART submission requirements.

---

### Priority 5 — Brasil

**Why Brasil is last:**
- Portuguese language requires a full translation effort — not just terminology adjustment.
- Brazil's regulatory framework (NRs) is the most complex and voluminous in LATAM — 38 normas regulamentadoras covering everything from basic safety to specific industries.
- eSocial integration is mandatory for AT and occupational health event reporting — requires technical API integration with the government system.
- Large market but high complexity and higher entry cost.

**Key regulatory additions:**

| Standard | Domain |
|---|---|
| NR-1 (updated 2024) | General occupational safety obligations |
| NR-6 | EPIs (PPE) |
| NR-9 | Physical risk exposure assessment |
| NR-15 | Unhealthy activities |
| NR-17 | Ergonomics |
| NR-35 | Work at height |
| RDC 275 | BPM for food |
| ANVISA regulations | Food safety regulator |

**New feature: eSocial Integration**
Brazil's eSocial is a mandatory government platform for labor and social security reporting. Occupational health events (SST events: accidents, occupational disease notifications, worker health exams) must be reported to eSocial via structured XML. This is a significant technical integration requiring:
- eSocial SST event schema compliance (S-2210, S-2220, S-2240, S-2245).
- Digital certificate signing (ICP-Brasil A1/A3).
- Submission status tracking and error handling.

---

## Technical Localization Requirements

### Standards Library Localization

Each country expansion adds a new data package to the standards library:
- Country-specific standards and regulations.
- Pre-translated clause text in the local language variant.
- Applicable company-size and industry filters.
- Regulatory calendar events for that country.

No code changes required — data migration only.

### Document and Report Templates

Each country requires localized versions of:
- Incident report form (FURAT → DIAT in Chile, etc.)
- Compliance evidence report
- Annual training program
- Certificate PDF template (logo placement, legal language)

Templates are stored as configurable layouts, not hardcoded PDFs.

### Language Variants

| Market | Language | Notes |
|---|---|---|
| Colombia, México, Perú, Chile, Argentina | Spanish (es) | Regional vocabulary differences (e.g., "empresa" vs. "compañía", "capacitación" vs. "formación") |
| Brasil | Portuguese (pt-BR) | Full translation required |

The platform uses a key-based translation system (i18n) from Phase 0. Regional Spanish variants are handled via a country-specific terminology override layer — e.g., the Colombian "ARL" becomes "ART" in Argentina and "Mutualidad" in Chile without requiring separate translation files.

### Billing and Legal

- Each country operates under a local legal entity or a reseller partnership.
- Local payment methods: PSE (Colombia), SPEI (México), Webpay (Chile), Mercado Pago (LATAM).
- Tax handling: IVA in Colombia/México/Chile, IGV in Peru, IVA in Argentina, ICMS/ISS in Brazil.
- Data residency: LATAM data privacy laws (Colombia Ley 1581, LGPD in Brazil) require careful data handling — consider per-country database clusters or at minimum configurable data residency.

---

## Go-To-Market Strategy Per Country

Rather than building a direct sales team in each country from scratch, the preferred entry model is:

1. **Consulting firm partnerships**: HSEQ consulting firms already have relationships with the target SME segment. A white-label or referral partner program allows rapid market penetration.
2. **ARL/Mutual insurance partnerships**: ARLs in Colombia are mandated to provide free SST support to their insured companies. A Quali integration with ARL tooling creates a distribution channel.
3. **Industry associations**: Chambers of commerce, food industry federations, and construction associations are trusted advisors to SMEs.

---

## Success Criteria

- A Mexican company can onboard, select NOM-035 + NOM-030, and run a psychosocial risk assessment with the validated questionnaire.
- A Chilean company can generate a DIAT incident report in the format required by their mutualidad.
- A Peruvian company can build their IPER matrix using the local methodology.
- Adding a new country's standards is achievable in under 2 weeks of work (data + templates, no code).
- The platform handles billing in local currency and local payment methods for each active country.
- Brazil eSocial SST event submission works end-to-end with digital certificate signing.
