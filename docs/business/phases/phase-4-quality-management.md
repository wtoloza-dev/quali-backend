# Phase 4 — Full Integrated Management System (IMS)

## Goal

Deliver the complete operational layer of Quali — the daily execution of safety and quality management across both verticals. At this point the platform stops being a compliance tracker and becomes the central operating system for HSEQ (Health, Safety, Environment, and Quality) in a Colombian company.

Phase 4 covers what happens every day on the production floor and in the workplace: accidents are reported, food non-conformances are registered, hazard matrices are managed, suppliers are qualified, product specs are controlled, and KPIs are tracked — all in one place, all connected.

---

## Scope

### SST Vertical — Occupational Safety Operations

#### Incident & Accident Management

Incidents and accidents are reported by any employee from any device. This is a mobile-first workflow — most reports come from a phone on the production floor or construction site.

- Report types: `accidente de trabajo` | `accidente con baja` | `enfermedad laboral` | `incidente` | `casi accidente`
- Report fields: date/time, location, worker involved, description, immediate cause, type of injury/illness
- Automatic classification by severity: `leve` | `grave` | `mortal`
- **Accidentes de trabajo** trigger the FURAT (Formato Único de Reporte de Accidente de Trabajo) generation — the legal form required by the ARL and Ministerio de Trabajo.
- Investigation workflow: immediate notification to SST coordinator → incident investigation → root cause analysis → corrective action (linked to Phase 3 CAR module).
- AT/EL rate calculations (accidentalidad indicators): incident frequency rate, severity rate, incidence rate — required for SG-SST annual reporting.

#### Hazard Matrix (Matriz de Peligros y Valoración de Riesgos)

The hazard matrix is the cornerstone document of any SG-SST system and arguably the most critical deliverable of the entire SST vertical.

- Create and maintain the company's hazard matrix following the **GTC 45** methodology (Colombian standard for hazard identification and risk assessment).
- Structure: `Process → Activity → Task → Hazard → Risk → Controls → Residual Risk`
- Hazard classification by GTC 45 categories: biological, physical, chemical, psychosocial, biomechanical, safety conditions, natural phenomena.
- Risk valuation: probability × severity = risk level (`aceptable` | `no aceptable` | `no aceptable o aceptable con controles`).
- Existing controls: engineering, administrative, PPE — with effectiveness rating.
- Residual risk after controls.
- Review triggers: when a new process is added, after an accident, or annually.
- The matrix is exportable as Excel (the traditional format) and as a structured PDF report.

#### EPP (Personal Protective Equipment) Control

- Define required PPE per job position, based on the hazard matrix.
- Track PPE assignment per employee: item, delivery date, condition, expected replacement date.
- Alert when PPE replacement is due.
- Generate delivery records (soporte de entrega de EPP) — a required document for SG-SST.

#### Occupational Health Surveillance Programs (PVVS)

- Register Programas de Vigilancia y Control de la Salud (PVVS) by exposure type: noise, dust, ergonomics, psychosocial, chemicals.
- Track employee enrollment in each program.
- Log periodic medical examination results and follow-up actions.
- Alert when periodic exams are due per enrolled employee.

#### Emergency Plan Management

- Document the company's emergency plan structure: brigades, evacuation routes, assembly points, emergency contacts.
- Track brigade members and their certifications (linked to Phase 1/2).
- Log drills: date, scenario, participants, duration, observations, improvements identified.
- Alert when the next mandatory drill is due (at least once per year per Decreto 1072).

---

### Food Quality Vertical — Operations

#### Non-Conformance Management (NCM)

Operators and quality staff register non-conformances directly from the production floor or receiving dock.

- Sources: `inspección interna` | `reclamo de cliente` | `desviación de proveedor` | `hallazgo de auditoría` | `resultado de laboratorio`
- Classification: by product, process area, severity (`leve` | `moderada` | `crítica`), and non-conformance type (BPM, HACCP, microbiological, physical, chemical).
- Lifecycle: `registrada → analizada → contenida → causa_raíz → acción_correctiva → cerrada`
- Disposition of non-conforming product: `liberado` | `reprocesado` | `devuelto` | `destruido` — with mandatory authorization.
- **Product recall workflow**: for critical NCMs, trigger a structured recall procedure with affected lot tracking, customer notification log, and regulatory notification (INVIMA) if required.
- Trend analysis: Pareto by type, area, supplier, product line.

#### HACCP Plan Management

- Create and maintain the HACCP plan for each product line.
- Hazard analysis table: ingredient/step → hazard type (biological, chemical, physical) → severity × probability → significant?
- Define Critical Control Points (CCPs) with critical limits, monitoring procedures, corrective actions, verification, and records.
- CCP monitoring records: log actual values against critical limits; out-of-limit values trigger automatic non-conformances.
- Prerequisite program (PPRO) management linked to BPM assessment in Phase 3.

#### Supplier Quality Management

- Supplier register with qualification status: `aprobado` | `condicional` | `suspendido` | `descalificado`
- Supplier qualification process: self-assessment questionnaire, supporting documents, audit (linked to Phase 3 audit module).
- Approved Supplier List (ASL) — required by ISO 22000 clause 7.1.6 and audited by INVIMA for critical raw materials.
- Incoming inspection: define inspection criteria and acceptable quality levels (AQL) per supplier and material.
- Supplier performance scorecard: on-time delivery, quality compliance rate, NCM frequency.
- Automatic suspension trigger when a supplier exceeds the configured NCM threshold.

#### Product & Raw Material Control

- Product register with technical specifications (organoleptic, physicochemical, microbiological parameters).
- Define control points per product: parameter, method, frequency, min/max limits, responsible role.
- Record inspection results. Out-of-spec results trigger automatic NCMs.
- Traceability: link raw material lots (with supplier and entry date) to finished product lots and dispatch records — enabling a full chain trace for INVIMA recall requirements.

---

### Cross-Vertical

#### BPM — Process Mapping

- Define key company processes as structured records linked to both verticals.
- Process attributes: name, owner, objective, inputs, outputs, linked standard clauses, KPIs.
- Optional: BPMN-lite visual representation (future UI feature).
- Process review cycle: define review frequency, track last review date, alert when due.

#### Unified KPI Dashboard

A single dashboard showing HSEQ health across both verticals, configurable by role:

| KPI | Vertical |
|---|---|
| Tasa de accidentalidad (AT frequency rate) | SST |
| Días perdidos por accidentes de trabajo | SST |
| % Cumplimiento SG-SST (Res. 0312 score) | SST |
| % Cumplimiento del plan de capacitación | SST + Food |
| Número de no conformidades abiertas | SST + Food |
| % CARs cerradas a tiempo | SST + Food |
| Índice de no conformidades por lote | Food |
| % Proveedores aprobados | Food |
| Score de auditoría BPM / ISO 22000 | Food |

- Configurable targets per KPI.
- Trend charts over configurable periods (monthly, quarterly, annual).
- PDCA cycle tracking: link improvement initiatives to specific KPIs.

#### Integrations (Phase 4+)

- Webhook integration for ERP product and lot data (SAP, TOTVS, Siesa — common in Colombia).
- Email digest reports (weekly KPI summary to HSEQ managers).
- REST API for lab instruments and third-party quality systems.
- ARL portal data export (some ARLs accept structured data uploads for AT reporting).

---

## Data Model (draft, key entities)

```
Incident
  id              UUID
  company_id      FK → Company
  type            enum: accidente | accidente_con_baja | enfermedad_laboral | incidente | casi_accidente
  severity        enum: leve | grave | mortal
  worker_id       FK → User
  reported_by     FK → User
  occurred_at     datetime
  location        string
  description     text
  furat_generated bool
  status          enum: reported | investigating | car_open | closed

HazardMatrix
  id              UUID
  company_id      FK → Company
  version         int
  methodology     string (default: "GTC 45")
  status          enum: draft | active | under_review
  last_reviewed   date

HazardEntry
  id              UUID
  matrix_id       FK → HazardMatrix
  process         string
  activity        string
  hazard_type     enum: biologico | fisico | quimico | psicosocial | biomecanico | condiciones_seguridad | fenomenos_naturales
  hazard          string
  risk            string
  probability     int (1–3)
  severity        int (1–4)
  risk_level      enum: aceptable | no_aceptable | no_aceptable_con_controles  (computed)
  controls        JSON
  residual_risk   enum

NonConformance
  id              UUID
  company_id      FK → Company
  vertical        enum: sst | food_quality
  source          enum: inspeccion | cliente | proveedor | auditoria | laboratorio
  severity        enum: leve | moderada | critica
  product_id      FK → Product | null
  area            string | null
  status          enum: registrada | analizada | contenida | causa_raiz | accion_correctiva | cerrada
  disposition     enum: liberado | reprocesado | devuelto | destruido | null
  registered_by   FK → User
  registered_at   datetime

HACCPPlan
  id              UUID
  company_id      FK → Company
  product_line    string
  version         int
  status          enum: draft | active | under_review

CCP
  id              UUID
  plan_id         FK → HACCPPlan
  step            string
  hazard          string
  critical_limit  string
  monitoring_proc string
  corrective_action text
  verification    text

CCPRecord
  id              UUID
  ccp_id          FK → CCP
  value           string
  within_limits   bool
  recorded_by     FK → User
  recorded_at     datetime

Supplier
  id              UUID
  company_id      FK → Company
  name            string
  nit             string | null
  category        string
  status          enum: aprobado | condicional | suspendido | descalificado
  score           float | null

Product
  id              UUID
  company_id      FK → Company
  name            string
  code            string
  specifications  JSON
  vertical        enum: food_quality | general

Process
  id              UUID
  company_id      FK → Company
  name            string
  owner_id        FK → User
  vertical        enum: sst | food_quality | general
  standard_clauses string[]
  kpis            JSON
  review_date     date | null
```

---

## Connection to All Previous Phases

| Phase | Connection |
|---|---|
| Phase 0 | All operational data is tenant-scoped; roles control who can register incidents, NCMs, and CCP records |
| Phase 1 | EPP delivery records and brigade certifications are verified certificates; CCP monitors must hold a valid HACCP certificate |
| Phase 2 | Incident root cause analysis can trigger mandatory safety training enrollment; NCM root cause can require BPM refresher course |
| Phase 3 | Audit findings feed into NCM and incident workflows; compliance gaps become prioritized improvement items on the PDCA board |

---

## Success Criteria

**SST:**
- A worker can report an accident from a mobile browser in under 2 minutes.
- The FURAT form is auto-generated from the incident report.
- The hazard matrix (GTC 45) can be built, maintained, and exported.
- AT indicators (frequency rate, severity rate) are calculated automatically from incident data.
- EPP delivery records are tracked per employee and alerted when due for replacement.

**Food Quality:**
- An operator can register a food non-conformance from the production floor.
- CCP monitoring values are logged and out-of-limit results trigger automatic non-conformances.
- Suppliers have qualification status and performance scores.
- Full lot traceability from raw material to finished product.

**Cross-vertical:**
- The unified KPI dashboard shows HSEQ health across both SST and food quality.
- A PDCA improvement cycle can be opened, tracked, and closed against a specific KPI.
- A quality manager can see the full non-conformance trend for the last 90 days across both verticals.
