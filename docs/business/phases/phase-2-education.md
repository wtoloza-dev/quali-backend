# Phase 2 — Education Platform

## Goal

Build an internal LMS (Learning Management System) for Colombian companies that need to train and certify their workforce across two regulatory domains: occupational safety (SG-SST) and food quality (BPM/HACCP). Employees complete courses, pass assessments, and automatically receive verifiable certificates — connecting directly to Phase 1's certification infrastructure.

This is not a generic e-learning platform. It is an opinionated training tool built around Colombian regulatory requirements, with pre-loaded course templates aligned to Resolución 0312 and Resolución 2674 obligations.

---

## Context: Training as a Regulatory Obligation

**In SST:**
Resolución 0312 de 2019 mandates a minimum annual training program for all employees. The SG-SST annual plan must include documented evidence of training completion. Specific topics are required:
- General safety induction for all new hires
- Risk-specific training (heights, chemicals, machinery, ergonomics)
- COPASST member training
- Emergency brigade formation and drills
- Manual materials handling

All of these require documented evidence that can be shown to the Ministerio de Trabajo.

**In food quality:**
Resolución 2674 de 2013 requires that food handlers receive ongoing training in:
- Personal hygiene and health habits
- BPM (Buenas Prácticas de Manufactura)
- Cleaning and disinfection procedures
- Food contamination control
- HACCP principles (for companies implementing HACCP)

Both domains have the same structural requirement: train → assess → certify → track expiration → recertify. The platform handles this loop for both.

---

## Scope

### Course Management

- Trainers, SST coordinators, and quality managers can create and publish courses.
- Course structure: `Course → Modules → Lessons`.
- Lesson types: rich text, embedded video (YouTube/Vimeo or hosted), file download (PDF, PPT).
- Courses are tagged with:
  - **Vertical**: `sst` | `food_quality` | `general`
  - **Standard linkage**: links to a specific standard or regulatory clause (e.g., Res. 0312, ISO 22000 clause 7.2)
  - **Required for roles**: e.g., this course is mandatory for all `employee` roles in `food_quality` vertical
- Courses have a configurable validity period — the issued certificate expires when the period ends.

### Pre-loaded Course Templates (System Library)

The platform ships with a library of course outlines aligned to Colombian regulations. Companies use them as-is or customize them.

**SST templates:**
- Inducción General SG-SST (mandatory for all new hires)
- Trabajo en Alturas — Nivel Básico (Res. 4272 de 2021)
- Manejo Seguro de Sustancias Químicas
- Prevención de Riesgos Ergonómicos
- Manejo Manual de Cargas
- Formación COPASST — Miembros del Comité
- Brigada de Emergencias — Primeros Auxilios
- Plan de Emergencias y Evacuación

**Food quality templates:**
- Higiene y Manipulación de Alimentos (Res. 2674)
- Buenas Prácticas de Manufactura (BPM)
- Limpieza y Desinfección — Operarios de Planta
- Principios HACCP — Monitores de PCC
- Control de Plagas — Personal Operativo
- Trazabilidad de Productos Alimenticios

Templates are data, not code. New templates are added as data entries.

### Enrollment

- Admins, SST coordinators, and quality managers can enroll employees manually.
- Bulk enrollment: assign a course to all employees in a department or with a specific role.
- Employees can self-enroll in courses marked as available for self-enrollment.
- Enrollment statuses: `not_started` → `in_progress` → `completed` | `failed`.
- Enrollment can be **mandatory** — the system tracks and reports non-completion.

### Assessments & Quizzes

- Each course has one final assessment (and optionally module-level quizzes).
- Question types: multiple choice (single answer), multiple choice (multiple answer), true/false.
- Configurable passing score per course (default: 80%).
- Configurable retake attempts (default: 3). After exhausting attempts, re-enrollment is required.
- All assessment results stored with timestamps — this is audit evidence.
- Question bank: questions can be pooled and randomized per attempt to prevent copying.

### Automatic Certificate Issuance

- On completion with a passing score, the certification module (Phase 1) is triggered automatically.
- The certificate is linked to the course, enrollment, and assessment result via `metadata`.
- The appropriate certificate template is selected based on the course's `vertical` and `template_id`.
- The employee receives a notification with their certificate and QR code.
- No manual intervention required from a manager.

### Annual SST Training Plan

A structured view specific to the SST vertical, aligned to Resolución 0312 requirements:

- Define the company's annual training plan with required courses, target audiences, and scheduled dates.
- Track plan execution: % completed, % overdue, by department.
- Generate the **Programa de Capacitación Anual** document required for SG-SST — exportable as PDF.
- Alert managers when mandatory training is behind schedule.

### Progress & Compliance Tracking

- **Employee view**: personal training dashboard showing completed courses, active certificates, pending mandatory courses, and upcoming expirations.
- **Manager view**: team completion rates per course, mandatory training compliance %, employees with expiring certificates.
- **Company view**: overall training compliance score, gap vs. regulatory minimum, ready-to-export evidence report.

### Recertification Workflow

- When a certificate approaches expiration (configurable alert threshold, e.g., 30 days before), the system sends an automatic reminder.
- The employee is automatically re-enrolled in the course (or the manager is prompted to re-enroll them).
- If a certificate expires without recertification, the employee's compliance status is flagged as `non-compliant` on the dashboard.

---

## Data Model (draft)

```
Course
  id                  UUID
  company_id          FK → Company (null = system template)
  title               string
  description         text
  vertical            enum: sst | food_quality | general
  regulatory_ref      string | null  (e.g. "Res. 0312 art. 9 numeral 2")
  certificate_template_id FK → CertificateTemplate | null
  validity_days       int | null
  passing_score       int (0–100, default 80)
  max_attempts        int (default 3)
  is_mandatory        bool
  status              enum: draft | published | archived
  is_system_template  bool

Module
  id          UUID
  course_id   FK → Course
  title       string
  order       int

Lesson
  id              UUID
  module_id       FK → Module
  title           string
  content_type    enum: text | video | file
  content         JSON
  order           int

Enrollment
  id              UUID
  user_id         FK → User
  course_id       FK → Course
  company_id      FK → Company
  is_mandatory    bool
  status          enum: not_started | in_progress | completed | failed
  enrolled_at     datetime
  completed_at    datetime | null

AssessmentResult
  id              UUID
  enrollment_id   FK → Enrollment
  score           int
  passed          bool
  attempt         int
  taken_at        datetime

TrainingPlan
  id              UUID
  company_id      FK → Company
  year            int
  status          enum: draft | active | closed

TrainingPlanItem
  id              UUID
  plan_id         FK → TrainingPlan
  course_id       FK → Course
  target_role     string | null
  target_dept     string | null
  scheduled_date  date | null
  completion_pct  float (computed)
```

---

## Connection to Phase 1

When an `Enrollment` reaches `completed` with a passing `AssessmentResult`, the system calls Phase 1's certificate issuance with:

```json
{
  "template_id": "<CertificateTemplate id>",
  "vertical": "sst",
  "metadata": {
    "course_id": "...",
    "enrollment_id": "...",
    "assessment_result_id": "...",
    "score": 87,
    "regulatory_ref": "Res. 0312 art. 9"
  }
}
```

Phase 1 certificates issued before Phase 2 existed remain valid. Phase 2 enriches new certificates with full training context.

## Connection to Phase 3

Compliance assessments in Phase 3 can query Phase 2 data as evidence. For example:

- Clause "6.2 — Competencia" of ISO 22000 requires proof that personnel are trained. The assessment can pull a completion report from Phase 2 as attached evidence.
- Res. 0312 item "Capacitación en el SG-SST" is automatically marked as evidenced when the annual training plan shows the required completion rate.

---

## Success Criteria

- An SST coordinator can create and publish an "Inducción General SG-SST" course.
- A quality manager can assign a BPM course to all food handling employees.
- An employee can complete lessons, take the assessment, and automatically receive their certificate.
- The annual SST training plan can be defined, tracked, and exported as a PDF.
- Managers see real-time training compliance rates by department.
- Expiring certificates trigger automatic recertification reminders.
- The system can generate an evidence report of training completion suitable for a Ministerio de Trabajo inspection.
