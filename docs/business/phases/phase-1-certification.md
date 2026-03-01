# Phase 1 — Digital Certification

## Goal

Allow companies to issue tamper-proof digital certificates for any purpose — SST inductions, food handler qualifications, COPASST training, equipment operation authorizations, emergency brigade membership — and allow anyone to verify their authenticity in real time via a QR code.

This is the first user-facing phase and the initial product offering. It is small enough to ship fast, generic enough to serve both verticals from day one, and creates an immediate proof of value for both SST coordinators and quality managers.

---

## Context: Why Certificates Matter in Both Verticals

**In SST (occupational safety):**
- Resolución 0312 requires documented evidence that workers received safety induction training.
- Workers who operate forklifts, work at height, handle chemicals, or form part of the emergency brigade must hold valid, verifiable authorizations.
- In a labor inspection (visita del Ministerio de Trabajo), the company must show certificates on demand — paper records are easily lost or faked.

**In food quality:**
- INVIMA inspections require evidence that food handlers have received hygiene and BPM training.
- HACCP plans require documented operator certification for CCP monitoring.
- Exporters must prove workforce training to international certification bodies.

A single certificate infrastructure serves both. The difference is configuration, not code.

---

## Scope

### Certificate Issuance

- Roles that can issue certificates: `admin`, `sst_coordinator`, `quality_manager`, `hseq_manager`, `trainer`.
- A certificate is a structured record rendered on demand — not a static file stored at rest.
- Certificate fields:
  - Recipient name and company
  - Certificate title (e.g., "Inducción SST", "Manipulador de Alimentos", "Trabajo en Alturas")
  - Issuing company and responsible person
  - Issue date and expiration date (optional)
  - Vertical tag: `sst` | `food_quality` | `general`
  - Standard linkage (optional): links to a clause in the standards library
  - A unique signed token for QR verification

### Certificate Types (pre-configured templates)

| Template | Vertical | Regulatory reference |
|---|---|---|
| Inducción SST | SST | Res. 0312 / Decreto 1072 |
| Trabajo en Alturas | SST | Res. 4272 de 2021 |
| Manejo de Químicos | SST | NTC 4435 |
| Brigada de Emergencias | SST | Res. 0256 de 2014 |
| Manipulación de Alimentos | Food | Res. 2674 de 2013 |
| HACCP — Monitor de PCC | Food | Codex Alimentarius |
| BPM — Higiene y Saneamiento | Food | Res. 2674 de 2013 |
| Genérico | Both | — |

Templates are data, not code. New types can be added without a deployment.

### QR Code Generation

- Each certificate gets a unique QR code at issuance.
- The QR encodes a public verification URL: `quali.app/verificar/<token>`.
- QR can be downloaded as PNG and embedded into a PDF or printed as a badge.

### Certificate Verification (Public)

- Public endpoint — no authentication required.
- Accessible from any smartphone by scanning the QR.
- Returns:
  - Certificate status: `válido`, `vencido`, `revocado`
  - Recipient name and issuing company
  - Certificate title and type
  - Issue date and expiration date
  - Time remaining until expiration (displayed as "Vence en 47 días")
  - Issuer name and position
- The page is designed to be shown at a factory gate, during a Ministerio de Trabajo inspection, or during an INVIMA visit.
- Response is in Spanish.

### Certificate Revocation

- Any authorized role can revoke a certificate with a mandatory reason.
- Revoked certificates show `REVOCADO` with the revocation date and reason on the verification page.
- Revocation is logged and auditable.

### Certificate PDF Export

- A styled, branded PDF can be generated for printing or email distribution.
- PDF includes the QR code, company logo, and all certificate fields.
- Language: Spanish.

### Bulk Issuance

- An authorized user can upload a CSV with a list of employees and issue certificates in batch.
- Useful for onboarding an entire production line after a training session.

---

## Data Model (draft)

```
Certificate
  id              UUID
  company_id      FK → Company
  recipient_id    FK → User
  title           string
  description     text | null
  vertical        enum: sst | food_quality | general
  template_id     FK → CertificateTemplate | null
  standard_clause string | null  (e.g. "Res. 0312 art. 9")
  issued_by       FK → User
  issued_at       datetime
  expires_at      datetime | null
  revoked_at      datetime | null
  revoked_by      FK → User | null
  revocation_reason text | null
  token           string (signed, unique, indexed)
  metadata        JSON  (course linkage placeholder for Phase 2)

CertificateTemplate
  id              UUID
  name            string
  vertical        enum
  default_validity_days int | null
  regulatory_ref  string | null
  is_system       bool  (true = platform-provided, false = company-custom)
```

---

## Key Design Decisions

**`metadata` is intentional.** Phase 2 will attach course completion data, assessment scores, and enrollment IDs to certificates. The field is a placeholder that avoids a schema migration later.

**`token` is signed, not random.** It is generated as a signed JWT-like structure containing the certificate ID and issue timestamp, making it verifiable without a database lookup in simple cases, and forgery-detectable in all cases.

**Templates are data, not code.** Adding a new certificate type for a new regulatory requirement (e.g., a new Ministerio de Trabajo resolution) is an admin data entry, not a development task.

---

## Connection to Phase 0

- All certificates are scoped to a `company_id` — enforced at issuance.
- The issuer role is validated against the company's RBAC configuration.
- Certificate templates are filtered by the company's active verticals.

---

## Success Criteria

- An SST coordinator can issue an "Inducción SST" certificate to a worker.
- A quality manager can issue a "Manipulación de Alimentos" certificate to a food handler.
- Scanning the QR on a phone opens a Spanish-language page with the certificate status.
- Expired and revoked certificates show the correct status with dates.
- The verification page loads without authentication.
- A batch of certificates can be issued via CSV upload.
- A PDF can be downloaded and printed for any certificate.
