"""Seed script: exact replica of production Manipulación Higiénica de Alimentos.

Creates company, course, 5 modules, 22 lessons (with full content from prod),
26 assessment questions, and publishes the course.

Requirements:
  - Backend running at http://localhost:8000 with SCOPE=local

Usage:
  uv run python scripts/seed_local_manipulacion.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import httpx

BASE_URL = "http://localhost:8000/api/v1"
SEED_USER_ID = "seed-local-dev"
DATA_DIR = Path(__file__).resolve().parent / "data"

client = httpx.Client(
    base_url=BASE_URL,
    timeout=30,
    follow_redirects=True,
    headers={"x-dev-seed": SEED_USER_ID},
)


def post(path: str, payload: dict) -> dict:
    """POST helper with error handling."""
    # Ensure trailing slash — redirects lose the POST body.
    if not path.endswith("/"):
        path += "/"
    r = client.post(path, json=payload)
    if r.status_code not in (200, 201):
        print(f"ERROR {r.status_code} POST {path}")
        print(r.text[:500])
        sys.exit(1)
    return r.json()


def load_json(filename: str) -> list:
    """Load a JSON data file from the data/ directory."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"ERROR: data file not found: {filepath}")
        sys.exit(1)
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


# ==============================================================
# 1. Company (same ID as production)
# ==============================================================

company_id = "01KK5QC4P7EN63HVG5KYR0VCK7"
print(f"Using company: {company_id}")

# ==============================================================
# 2. Course
# ==============================================================

print("Creating course...")
course = post(f"/companies/{company_id}/education/courses", {
    "title": "Manipulación Higiénica de Alimentos",
    "description": (
        "Aprende a manipular alimentos de forma segura. Este curso te prepara "
        "para proteger la salud de tus clientes y cumplir con la Resolución 2674 "
        "de 2013 del Ministerio de Salud de Colombia."
    ),
    "vertical": "food_quality",
    "regulatory_ref": "Resolución 2674 de 2013",
    "validity_days": 365,
    "visibility": "public",
})
course_id = course["id"]
print(f"  Course: {course_id}")

# ==============================================================
# 3. Modules & Lessons
# ==============================================================

MODULES = load_json("seed_manipulacion_modules.json")
module_ids: dict[int, str] = {}

for mod in MODULES:
    print(f"\nModule {mod['order']}: {mod['title']}...")
    module = post(
        f"/companies/{company_id}/education/courses/{course_id}/modules",
        {"title": mod["title"], "order": mod["order"]},
    )
    mod_id = module["id"]
    module_ids[mod["order"]] = mod_id
    print(f"  -> {mod_id}")

    for lesson in mod["lessons"]:
        print(f"  Lesson {lesson['order']}: {lesson['title']}")
        post(
            f"/companies/{company_id}/education/courses/{course_id}/modules/{mod_id}/lessons",
            {
                "title": lesson["title"],
                "order": lesson["order"],
                "is_preview": lesson["is_preview"],
                "content": lesson["content"],
            },
        )

# ==============================================================
# 4. Questions
# ==============================================================

print("\nCreating questions...")

QUESTIONS = load_json("seed_manipulacion_questions.json")

for q in QUESTIONS:
    mod_order = q.pop("module_order")
    q["module_id"] = module_ids[mod_order]
    print(f"  Q{q['order']} (M{mod_order}) [{q['question_type']}]: {q['text'][:55]}...")
    post(
        f"/companies/{company_id}/education/courses/{course_id}/questions",
        q,
    )

# ==============================================================
# 5. Publish
# ==============================================================

print("\nPublishing course...")
post(f"/companies/{company_id}/education/courses/{course_id}/publish", {})

total_lessons = sum(len(m["lessons"]) for m in MODULES)

print()
print("=" * 60)
print("SEED COMPLETE!")
print(f"  Company ID:  {company_id}")
print(f"  Course ID:   {course_id}")
print(f"  Modules:     {len(MODULES)}")
print(f"  Lessons:     {total_lessons}")
print(f"  Questions:   {len(QUESTIONS)}")
print(f"  Status:      PUBLISHED")
print("=" * 60)
