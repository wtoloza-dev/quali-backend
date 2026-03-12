"""Seed script: Module 1 — El Enemigo Invisible.

Seeds the curated 'Manipulación Higiénica de Alimentos' course with
Module 1 (4 lessons) and its assessment questions.

Requirements:
  - The backend must be running at http://localhost:8000
  - Auth must be bypassed (SCOPE=local dev mode)

Usage:
  uv run python scripts/seed_m1_el_enemigo_invisible.py

To target production, set the BASE_URL environment variable:
  BASE_URL=https://api.quali.co uv run python scripts/seed_m1_el_enemigo_invisible.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import httpx


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/api/v1")
COURSES_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "quali-courses"
    / "manipulacion-higienica-alimentos"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SEED_USER_ID = "seed-local-dev"

client = httpx.Client(
    base_url=BASE_URL,
    timeout=30,
    follow_redirects=True,
    headers={"x-dev-seed": SEED_USER_ID},
)


def post(path: str, json: dict) -> dict:
    """POST helper with error handling."""
    r = client.post(path, json=json)
    if r.status_code not in (200, 201):
        print(f"ERROR {r.status_code} POST {path}")
        print(r.text)
        sys.exit(1)
    return r.json()


def read_md(filepath: Path) -> str:
    """Read a markdown file and return its content."""
    if not filepath.exists():
        print(f"  WARNING: file not found: {filepath}")
        return f"# Contenido pendiente\n\nArchivo no encontrado: {filepath.name}"
    return filepath.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Create company (idempotent — will fail if already exists)
# ---------------------------------------------------------------------------

print("Creating company...")
company = post(
    "/companies",
    {
        "name": "Quali Demo",
        "slug": "quali-demo",
        "company_type": "organization",
        "email": "demo@quali.co",
        "country": "CO",
        "tax": {
            "tax_type": "NIT",
            "tax_id": "900000000-0",
        },
    },
)
company_id = company["id"]
print(f"  Company: {company_id}")

# ---------------------------------------------------------------------------
# 2. Create course
# ---------------------------------------------------------------------------

print("Creating course...")
course = post(
    f"/companies/{company_id}/education/courses",
    {
        "title": "Manipulación Higiénica de Alimentos",
        "description": (
            "Aprende a manipular alimentos de forma segura. Este curso te prepara "
            "para proteger la salud de tus clientes y cumplir con la Resolución 2674 "
            "de 2013 del Ministerio de Salud de Colombia. Diseñado para personal de "
            "restaurantes, panaderías, cafeterías y negocios de alimentos."
        ),
        "vertical": "food_quality",
        "regulatory_ref": "Resolución 2674 de 2013",
        "validity_days": 365,
        "passing_score": 70,
        "max_attempts": 3,
        "is_mandatory": True,
        "visibility": "public",
    },
)
course_id = course["id"]
print(f"  Course: {course_id}")

# ---------------------------------------------------------------------------
# 3. Module 1: El Enemigo Invisible
# ---------------------------------------------------------------------------

MODULE_DIR = COURSES_DIR / "modulo-01-el-enemigo-invisible"

print("Creating Module 1: El Enemigo Invisible...")
module = post(
    f"/companies/{company_id}/education/courses/{course_id}/modules",
    {
        "title": "El Enemigo Invisible",
        "order": 1,
    },
)
module_id = module["id"]
print(f"  Module: {module_id}")

LESSONS = [
    {
        "title": "La hamburguesa que mató a 4 niños",
        "order": 1,
        "file": "leccion-01-la-hamburguesa-que-mato.md",
        "is_preview": True,
    },
    {
        "title": "¿Qué son las ETA? Lo que pasa cuando falla la higiene",
        "order": 2,
        "file": "leccion-02-que-son-las-eta.md",
        "is_preview": True,
    },
    {
        "title": "Los tres villanos: bacterias, virus y parásitos",
        "order": 3,
        "file": "leccion-03-los-tres-villanos.md",
        "is_preview": True,
    },
    {
        "title": "Casos en Colombia: lo que dice el INS",
        "order": 4,
        "file": "leccion-04-casos-colombia.md",
        "is_preview": True,
    },
]

for lesson in LESSONS:
    content = read_md(MODULE_DIR / lesson["file"])
    print(f"  Creating lesson {lesson['order']}: {lesson['title']}...")
    les = post(
        f"/companies/{company_id}/education/courses/{course_id}/modules/{module_id}/lessons",
        {
            "title": lesson["title"],
            "content": [
                {
                    "type": "text",
                    "order": 1,
                    "body": content,
                }
            ],
            "order": lesson["order"],
            "is_preview": lesson["is_preview"],
        },
    )
    print(f"    Lesson: {les['id']}")

# ---------------------------------------------------------------------------
# 4. Module 1 — Assessment questions
# ---------------------------------------------------------------------------

print("Creating Module 1 questions...")

QUESTIONS = [
    # Q1 — Scenario (uses MC format with narrative in text)
    {
        "text": (
            "Trabajas en la cocina de un restaurante. Al mediodía recibes un pedido "
            "de carne molida. Al tocarla notas que está tibia. El proveedor te dice: "
            '"Tranquilo, la acabo de sacar del camión."\n'
            "\n---\n\n"
            "¿Qué debes hacer?"
        ),
        "question_type": "multiple_choice_single",
        "order": 1,
        "config": {
            "type": "multiple_choice",
            "options": [
                {
                    "text": "Aceptarla y refrigerarla inmediatamente — con frío se arregla",
                    "is_correct": False,
                },
                {
                    "text": "Rechazarla. La carne molida debe llegar a máximo 4°C. Si está tibia, la cadena de frío se rompió y puede haber bacterias como E. coli multiplicándose",
                    "is_correct": True,
                },
                {
                    "text": "Aceptarla pero cocinarla de inmediato para matar cualquier bacteria",
                    "is_correct": False,
                },
                {"text": "Olerla y si no huele mal, aceptarla", "is_correct": False},
            ],
        },
    },
    # Q2 — Standard MC (from lesson 1.1)
    {
        "text": "¿Por qué la carne molida es más peligrosa que un filete entero?",
        "question_type": "multiple_choice_single",
        "order": 2,
        "config": {
            "type": "multiple_choice",
            "options": [
                {
                    "text": "Porque tiene más grasa y la grasa atrae más bacterias",
                    "is_correct": False,
                },
                {
                    "text": "Porque al moler la carne, las bacterias de la superficie se mezclan por todo el interior",
                    "is_correct": True,
                },
                {
                    "text": "Porque la carne molida siempre viene de animales más viejos",
                    "is_correct": False,
                },
                {
                    "text": "No es más peligrosa, el riesgo es el mismo",
                    "is_correct": False,
                },
            ],
        },
    },
    # Q3 — True/False (from lesson 1.2)
    {
        "text": "En una intoxicación alimentaria, calentar la comida a alta temperatura elimina el peligro porque mata tanto la bacteria como la toxina.",
        "question_type": "true_false",
        "order": 3,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Verdadero", "is_correct": False},
                {
                    "text": "Falso — el calor puede matar la bacteria, pero la toxina que ya dejó en la comida NO se destruye con el calor",
                    "is_correct": True,
                },
            ],
        },
    },
    # Q4 — Standard MC (from lesson 1.2)
    {
        "text": "¿Cuál de estas es la diferencia clave entre una infección alimentaria y una intoxicación alimentaria?",
        "question_type": "multiple_choice_single",
        "order": 4,
        "config": {
            "type": "multiple_choice",
            "options": [
                {
                    "text": "La infección es causada por virus y la intoxicación por bacterias",
                    "is_correct": False,
                },
                {
                    "text": "En la infección el microorganismo vivo te enferma; en la intoxicación te enferma la toxina que el microorganismo dejó en la comida",
                    "is_correct": True,
                },
                {
                    "text": "La intoxicación es más grave que la infección",
                    "is_correct": False,
                },
                {"text": "No hay diferencia real, son lo mismo", "is_correct": False},
            ],
        },
    },
    # Q5 — Standard MC (from lesson 1.3 — FATTOM)
    {
        "text": "¿Cuál es el rango de la 'zona de peligro' donde las bacterias se multiplican más rápido?",
        "question_type": "multiple_choice_single",
        "order": 5,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Entre 0°C y 25°C", "is_correct": False},
                {"text": "Entre 5°C y 60°C", "is_correct": True},
                {"text": "Entre 10°C y 45°C", "is_correct": False},
                {"text": "Entre -18°C y 30°C", "is_correct": False},
            ],
        },
    },
    # Q6 — Scenario (from lesson 1.3 — Norovirus)
    {
        "text": (
            'Un compañero de la cocina llegó con diarrea. Te dice: "Ya me tomé una '
            'pastilla, estoy bien. Si me voy me descuentan el día."\n'
            "\n---\n\n"
            "¿Qué le dirías?"
        ),
        "question_type": "multiple_choice_single",
        "order": 6,
        "config": {
            "type": "multiple_choice",
            "options": [
                {
                    "text": "Que use doble guante y tapabocas y siga trabajando",
                    "is_correct": False,
                },
                {
                    "text": "Que no toque alimentos listos para consumo pero puede lavar platos",
                    "is_correct": False,
                },
                {
                    "text": "Que debe reportar al supervisor y ser retirado de la manipulación de alimentos — un solo manipulador enfermo con Norovirus puede contagiar a cientos de clientes",
                    "is_correct": True,
                },
                {
                    "text": "Que se lave bien las manos con gel antibacterial y continúe",
                    "is_correct": False,
                },
            ],
        },
    },
    # Q7 — Standard MC (from lesson 1.3 — Staphylococcus)
    {
        "text": "¿Qué hace especialmente peligroso al Staphylococcus aureus en la cocina?",
        "question_type": "multiple_choice_single",
        "order": 7,
        "config": {
            "type": "multiple_choice",
            "options": [
                {
                    "text": "Que solo se encuentra en alimentos importados",
                    "is_correct": False,
                },
                {
                    "text": "Que produce una toxina que NO se destruye con el calor — aunque hiervas la comida, la toxina sigue ahí",
                    "is_correct": True,
                },
                {
                    "text": "Que solo afecta a niños menores de 5 años",
                    "is_correct": False,
                },
                {
                    "text": "Que cambia el color de los alimentos y se puede detectar fácilmente",
                    "is_correct": False,
                },
            ],
        },
    },
    # Q8 — True/False (from lesson 1.3 — Norovirus vs gel)
    {
        "text": "El gel antibacterial es suficiente para eliminar el Norovirus de las manos.",
        "question_type": "true_false",
        "order": 8,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Verdadero", "is_correct": False},
                {
                    "text": "Falso — el Norovirus resiste el alcohol en gel. Solo el lavado con jabón y agua lo elimina",
                    "is_correct": True,
                },
            ],
        },
    },
    # Q9 — Standard MC (from lesson 1.4 — Colombia stats)
    {
        "text": "Según el INS, ¿cuáles son los dos lugares donde ocurren MÁS brotes de ETA en Colombia?",
        "question_type": "multiple_choice_single",
        "order": 9,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Hospitales y clínicas", "is_correct": False},
                {
                    "text": "Hogares y restaurantes/establecimientos de comida",
                    "is_correct": True,
                },
                {"text": "Supermercados y plazas de mercado", "is_correct": False},
                {"text": "Colegios y universidades", "is_correct": False},
            ],
        },
    },
    # Q10 — Scenario (from lesson 1.4 — practical Colombia case)
    {
        "text": (
            "Es domingo y tu familia prepara un almuerzo grande. Tu mamá deja el "
            "pollo crudo en una bolsa plástica sobre el mesón de la cocina mientras "
            "prepara el resto. El jugo del pollo gotea y toca las verduras que van "
            "para la ensalada.\n"
            "\n---\n\n"
            "¿Cuál es el riesgo y qué deberían hacer?"
        ),
        "question_type": "multiple_choice_single",
        "order": 10,
        "config": {
            "type": "multiple_choice",
            "options": [
                {
                    "text": "No hay riesgo si las verduras se lavan con agua antes de servirlas",
                    "is_correct": False,
                },
                {
                    "text": "Hay riesgo de contaminación cruzada — bacterias como Salmonella del jugo del pollo pasaron a las verduras. Deben descartarlas o lavarlas y desinfectarlas con solución de hipoclorito",
                    "is_correct": True,
                },
                {"text": "Solo hay riesgo si el pollo huele mal", "is_correct": False},
                {
                    "text": "Es seguro si cocinan las verduras junto con el pollo",
                    "is_correct": False,
                },
            ],
        },
    },
]

for q in QUESTIONS:
    payload = {
        "text": q["text"],
        "question_type": q["question_type"],
        "order": q["order"],
        "module_id": module_id,
        "config": q["config"],
        "randomize": True,
    }
    print(f"  Q{q['order']}: {q['text'][:60]}...")
    post(
        f"/companies/{company_id}/education/courses/{course_id}/questions",
        payload,
    )

# ---------------------------------------------------------------------------
# 5. Done (do NOT publish yet — more modules to come)
# ---------------------------------------------------------------------------

print()
print("=" * 60)
print("MODULE 1 SEED COMPLETE!")
print(f"  Company ID:  {company_id}")
print(f"  Course ID:   {course_id}")
print(f"  Module ID:   {module_id}")
print(f"  Lessons:     {len(LESSONS)}")
print(f"  Questions:   {len(QUESTIONS)}")
print("  Status:      DRAFT (not published yet)")
print("=" * 60)
