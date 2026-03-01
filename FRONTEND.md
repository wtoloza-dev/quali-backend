# Quali Frontend — MVP Implementation Plan

## Stack

| Tool | Purpose |
|---|---|
| Next.js 15 (App Router) | Framework |
| next-auth v5 (Auth.js) | Google OAuth + session |
| TanStack Query | Server state / API calls |
| shadcn/ui + Tailwind | UI components |
| Zod | Form validation |

---

## Google OAuth — How it works

```
User clicks "Sign in with Google"
        │
        ▼
next-auth redirects to Google consent screen
        │
        ▼
Google returns id_token (JWT with email, name, picture)
        │
        ▼
next-auth sends id_token to backend   ← NEW ENDPOINT NEEDED
  POST /api/v1/iam/google
  { "id_token": "eyJ..." }
        │
        ▼
Backend verifies with Google, finds/creates user,
returns Quali JWT
        │
        ▼
next-auth stores Quali JWT in session cookie
        │
        ▼
All API calls use: Authorization: Bearer <quali_jwt>
```

### New backend endpoint required

```
POST /api/v1/iam/google
Body:     { "id_token": "string" }
Response: { "access_token": "string", "token_type": "bearer" }
```

Backend logic:
1. Verify `id_token` with Google (`google-auth` library)
2. Extract `email`, `name`, `sub` (Google user ID)
3. Find user by email → if not found, create user + credentials
4. Return Quali JWT (same shape as `/api/v1/iam/login`)

---

## Pages

### 1. `/` — Login
**Auth:** Public

| Element | Description |
|---|---|
| Logo + tagline | "Capacita tu equipo. Cumple la norma." |
| Google sign-in button | Triggers next-auth Google flow |

**Endpoints:** None (handled by next-auth)

---

### 2. `/dashboard` — Home
**Auth:** Required

| Element | Description |
|---|---|
| Welcome card | User name + company name |
| Active enrollments | List of courses in progress |
| Compliance status | % employees with BPM certificate |
| Quick actions | "Add employee", "Enroll team" |

**Endpoints:**
```
GET  /api/v1/companies/{company_id}/education/enrollments/
GET  /api/v1/companies/{company_id}/certificates/
GET  /api/v1/companies/{company_id}/members
```

---

### 3. `/courses` — Course catalog
**Auth:** Required

| Element | Description |
|---|---|
| Course card | BPM course (Resolución 2674) |
| Status badge | Not started / In progress / Completed |
| Enroll button | Creates enrollment |

**Endpoints:**
```
GET  /api/v1/companies/{company_id}/education/courses/
POST /api/v1/companies/{company_id}/education/enrollments/
```

---

### 4. `/courses/[courseId]` — Course detail
**Auth:** Required

| Element | Description |
|---|---|
| Course description | Title, objectives, duration |
| Module list | Accordion with lessons |
| Start / Continue button | Links to first pending lesson |
| Progress bar | % completed |

**Endpoints:**
```
GET  /api/v1/companies/{company_id}/education/courses/{course_id}
GET  /api/v1/companies/{company_id}/education/courses/{course_id}/modules
GET  /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}
```

---

### 5. `/courses/[courseId]/learn/[lessonId]` — Lesson viewer
**Auth:** Required

| Element | Description |
|---|---|
| Lesson content | Video, text, or PDF embed |
| Sidebar | Module/lesson navigation |
| Next lesson button | Advances to next lesson |
| Finish module button | Shows on last lesson |

**Endpoints:**
```
GET  /api/v1/companies/{company_id}/education/courses/{course_id}/modules/{module_id}/lessons/{lesson_id}
PATCH /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}/status
```

---

### 6. `/courses/[courseId]/quiz` — Assessment
**Auth:** Required

| Element | Description |
|---|---|
| Questions list | Multiple choice / true-false |
| Submit button | Sends all answers at once |
| Result screen | Score + pass/fail + certificate link |

**Endpoints:**
```
GET  /api/v1/companies/{company_id}/education/courses/{course_id}/questions
POST /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}/attempts
```

---

### 7. `/certificates` — My certificates
**Auth:** Required

| Element | Description |
|---|---|
| Certificate card | Course name, issue date, expiration |
| Download/share button | Opens public verify URL |

**Endpoints:**
```
GET  /api/v1/companies/{company_id}/certificates/
```

---

### 8. `/certificates/verify/[token]` — Public certificate
**Auth:** Public (no login required)

| Element | Description |
|---|---|
| Certificate details | Name, course, date, issuer |
| Valid/Revoked badge | Visual status |
| QR scannable page | Auditor-friendly layout |

**Endpoints:**
```
GET  /api/v1/certificates/verify/{token}
```

---

### 9. `/team` — Team management
**Auth:** Required (OWNER or ADMIN)

| Element | Description |
|---|---|
| Employee list | Name, email, BPM status |
| Add employee button | Invite by email |
| Enroll all button | Bulk enrollment in BPM course |
| Compliance badge | Certified / Expiring / Missing |

**Endpoints:**
```
GET  /api/v1/companies/{company_id}/members
POST /api/v1/companies/{company_id}/members
POST /api/v1/companies/{company_id}/education/enrollments/   (per user)
GET  /api/v1/companies/{company_id}/certificates/
```

---

## Build order

```
Week 1 — Auth + shell
  1. next-auth Google setup
  2. Backend: POST /api/v1/iam/google
  3. App layout (sidebar, nav, auth guard)

Week 2 — Core learning flow
  4. /courses  (catalog)
  5. /courses/[id]  (detail + enroll)
  6. /courses/[id]/learn/[lessonId]  (lesson viewer)

Week 3 — Assessment + Certificate
  7. /courses/[id]/quiz
  8. /certificates
  9. /certificates/verify/[token]  (public)

Week 4 — Team
  10. /dashboard
  11. /team  (add employees, bulk enroll)
```

---

## Environment variables (Next.js)

```env
NEXTAUTH_SECRET=
NEXTAUTH_URL=http://localhost:3000

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

NEXT_PUBLIC_API_URL=http://localhost:8000
```
