# Phase 3 — Compliance & Audits

## Goal

Give SST coordinators and quality managers a structured tool to assess their company's compliance against applicable standards and regulations, plan and execute audits, manage corrective actions, and maintain the evidence trail required by the Ministerio de Trabajo, INVIMA, and ISO certification bodies.

This phase serves both verticals simultaneously. The same audit and corrective action infrastructure is used for an SG-SST internal audit and for an ISO 22000 gap assessment — the difference is the standard selected, not the tool.

This phase is the bridge between the people side (training, certifications — Phases 1 and 2) and the live operational system built in Phase 4.

---

## Scope

### Standards Library

The platform ships with a pre-loaded, structured library of applicable Colombian and international standards. Standards are data — adding a new one requires no code change.

**Initial standards loaded at launch:**

| Standard | Domain | Type |
|---|---|---|
| SG-SST — Resolución 0312 de 2019 | Occupational Safety | Colombian mandatory |
| Decreto 1072 de 2015 (SST chapters) | Occupational Safety | Colombian mandatory |
| ISO 45001:2018 | Occupational Safety | International |
| Resolución 2674 de 2013 (BPM) | Food Quality | Colombian mandatory |
| ISO 22000:2018 | Food Quality | International |
| HACCP — Codex Alimentarius | Food Quality | International |
| ISO 9001:2015 | General Quality | International |

Each standard is modeled as a hierarchical clause tree. For example:

```
Resolución 0312
  └── Artículo 9 — Estándares mínimos para empresas de 11 a 50 trabajadores
        ├── Numeral 1 — Asignación de persona que diseña el SG-SST
        ├── Numeral 2 — Afiliación al SGSS
        ├── Numeral 3 — Conformación COPASST
        ...
```

Companies select which standards apply to them. Their dashboard, compliance assessments, and audit checklists are built from that selection.

### Compliance Gap Assessment

- An authorized user initiates a self-assessment against one or more selected standards.
- For each clause/requirement, they record: `cumple` | `cumple parcialmente` | `no cumple` | `no aplica`.
- Evidence can be attached per clause: documents, photos, training reports from Phase 2, certificates from Phase 1.
- A gap analysis report is generated automatically, showing compliance percentage by section and a risk-weighted list of gaps.
- Assessments are versioned — a company can run the same assessment quarterly and track improvement over time.

**Special case — Resolución 0312 scoring:**
Res. 0312 uses a weighted scoring system (0–100 points) with defined thresholds:
- ≥ 86%: Critical risk (paradoxically labeled — this is the passing score in the resolution's scale)
- 61–85%: Moderately acceptable
- ≤ 60%: Critical — subject to Ministerio de Trabajo intervention

The platform calculates this score automatically and flags the risk level.

### Audit Management

Audits can be internal (self-audits, COPASST inspections) or external (certification body, customer audit, Ministerio de Trabajo, INVIMA inspection).

- **Audit planning**: define scope, applicable standard, auditor(s), scheduled date, checklist source.
- **Audit execution**: checklist-based findings per clause, with notes and evidence attachments.
- **Finding classification**:
  - `conformidad` — requirement met
  - `observación` — minor opportunity for improvement, no non-conformance
  - `no conformidad menor` — requirement partially met, corrective action required
  - `no conformidad mayor` — requirement not met or critical gap, immediate action required
- **Audit report**: auto-generated on completion, including findings summary, evidence, and required actions. Exportable as PDF.

**COPASST Inspection support (SST-specific):**
- COPASST is legally required to conduct monthly workplace inspections.
- Pre-built inspection checklist template for common workplace hazards.
- Inspection results feed directly into the corrective action workflow.

### Corrective Action Requests (CAR / Acción Correctiva)

Non-conformances from audits, assessments, or COPASST inspections automatically generate a corrective action record.

CAR lifecycle:
```
abierta → en análisis → acción planificada → implementada → verificada → cerrada
```

Each stage requires:
- **En análisis**: root cause analysis (5-Why or Ishikawa diagram fields)
- **Acción planificada**: action plan with responsible person, due date, and required resources
- **Implementada**: implementation evidence attachment
- **Verificada**: effectiveness verification by the auditor or coordinator
- **Cerrada**: closure with final summary

Overdue CARs are flagged on the dashboard and trigger alerts to the responsible person and their manager.

**Training-triggered CARs (connection to Phase 2):**
If the root cause of a non-conformance is identified as a knowledge or competence gap, the CAR can trigger mandatory enrollment in a relevant course — creating a closed loop between compliance management and training.

### Document Control

- Upload and version-controlled documents linked to standard clauses.
- Each document has: title, version, responsible owner, review date, applicable standards.
- Document statuses: `draft` | `active` | `under_review` | `obsolete`.
- Automatic alerts when a document approaches its review date.
- Obsolete versions are retained for audit trail but flagged as superseded.
- Core document types pre-categorized:
  - **SST**: Política SST, Matriz de Peligros, Plan de Emergencias, Programa de Capacitación, Reglamento de Higiene
  - **Food**: Manual de BPM, Plan HACCP, Procedimientos de Limpieza y Desinfección, Fichas Técnicas

---

## Data Model (draft)

```
Standard
  id              UUID
  name            string
  code            string (e.g. "RES_0312_2019")
  domain          enum: sst | food_quality | general_quality
  type            enum: colombian_law | international_iso | other
  version         string
  effective_date  date
  clauses         JSON  (hierarchical requirement tree)
  is_system       bool

ComplianceAssessment
  id              UUID
  company_id      FK → Company
  standard_id     FK → Standard
  period          string (e.g. "Q1-2025")
  status          enum: draft | in_progress | completed
  score           float | null  (calculated on completion)
  risk_level      enum: acceptable | moderate | critical | null
  assessed_by     FK → User
  assessed_at     datetime | null

ClauseAssessment
  id              UUID
  assessment_id   FK → ComplianceAssessment
  clause_ref      string (e.g. "Art. 9 Num. 3")
  clause_weight   float | null  (for weighted standards like Res. 0312)
  status          enum: cumple | parcial | no_cumple | na
  notes           text | null
  evidence_files  string[]

Audit
  id              UUID
  company_id      FK → Company
  type            enum: internal | external | copasst_inspection
  standard_id     FK → Standard
  auditor_id      FK → User
  scheduled_at    datetime
  started_at      datetime | null
  completed_at    datetime | null
  status          enum: planned | in_progress | completed | cancelled

AuditFinding
  id              UUID
  audit_id        FK → Audit
  clause_ref      string
  classification  enum: conformidad | observacion | nc_menor | nc_mayor
  description     text
  evidence_files  string[]

CorrectiveAction
  id                  UUID
  company_id          FK → Company
  source              enum: audit | assessment | copasst | incident | spontaneous
  source_id           UUID | null  (FK to audit finding, assessment clause, etc.)
  title               string
  description         text
  assigned_to         FK → User
  due_date            date
  status              enum: abierta | en_analisis | planificada | implementada | verificada | cerrada
  root_cause_method   enum: five_why | ishikawa | other | null
  root_cause          text | null
  action_plan         text | null
  evidence_files      string[]
  course_triggered_id FK → Course | null  (Phase 2 linkage)
  closed_at           datetime | null

Document
  id              UUID
  company_id      FK → Company
  title           string
  category        enum: policy | procedure | plan | record | form | other
  vertical        enum: sst | food_quality | general
  version         string
  status          enum: draft | active | under_review | obsolete
  owner_id        FK → User
  review_date     date
  standard_clauses string[]
  file_url        string
```

---

## Connection to Previous Phases

| Phase | Connection |
|---|---|
| Phase 0 | All compliance data is tenant-scoped; roles define who can initiate assessments and audits |
| Phase 1 | Certificate records can be attached as evidence for "competence" clauses (e.g., Res. 0312 training items) |
| Phase 2 | Training completion reports serve as compliance evidence; knowledge-gap CARs trigger course enrollment |

---

## Success Criteria

- An SST coordinator can run a Resolución 0312 self-assessment and get the official weighted score.
- A quality manager can run a BPM (Res. 2674) gap assessment with evidence attached per clause.
- A COPASST inspection can be planned, executed, and closed with findings documented.
- Non-conformances generate CARs tracked through full lifecycle to closure with effectiveness verification.
- Documents are version-controlled, linked to clauses, and alert owners before review deadlines.
- The system can generate an audit report PDF suitable for submission to INVIMA or the Ministerio de Trabajo.
- Compliance trend over time is visible per standard per quarter.
