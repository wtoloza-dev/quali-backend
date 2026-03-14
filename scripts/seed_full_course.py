"""Seed script: Full course — Manipulación Higiénica de Alimentos.

Seeds the complete course with 5 modules, 22 lessons, and 25 assessment
questions (5 per module). Publishes the course at the end.

Requirements:
  - The backend must be running at http://localhost:8000
  - Auth must be bypassed (SCOPE=local dev mode)

Usage:
  uv run python scripts/seed_full_course.py

To target production, set the BASE_URL environment variable:
  BASE_URL=https://api.quali.co uv run python scripts/seed_full_course.py
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
# 1. Create company
# ---------------------------------------------------------------------------

print("Creating company...")
company = post("/companies", {
    "name": "Quali Demo",
    "slug": "quali-demo",
    "company_type": "organization",
    "email": "demo@quali.co",
    "country": "CO",
    "tax": {
        "tax_type": "NIT",
        "tax_id": "900000000-0",
    },
})
company_id = company["id"]
print(f"  Company: {company_id}")

# ---------------------------------------------------------------------------
# 2. Create course
# ---------------------------------------------------------------------------

print("Creating course...")
course = post(f"/companies/{company_id}/education/courses", {
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
})
course_id = course["id"]
print(f"  Course: {course_id}")

# ---------------------------------------------------------------------------
# 3. Modules and Lessons
# ---------------------------------------------------------------------------

MODULES = [
    {
        "title": "El Enemigo Invisible",
        "order": 1,
        "dir": "modulo-01-el-enemigo-invisible",
        "lessons": [
            {"title": "La hamburguesa que mató a 4 niños", "order": 1, "file": "leccion-01-la-hamburguesa-que-mato.md"},
            {"title": "¿Qué son las ETA? Lo que pasa cuando falla la higiene", "order": 2, "file": "leccion-02-que-son-las-eta.md"},
            {"title": "Los tres villanos: bacterias, virus y parásitos", "order": 3, "file": "leccion-03-los-tres-villanos.md"},
            {"title": "Casos en Colombia: lo que dice el INS", "order": 4, "file": "leccion-04-casos-colombia.md"},
        ],
    },
    {
        "title": "Tu Cuerpo, Tu Herramienta",
        "order": 2,
        "dir": "modulo-02-tu-cuerpo-tu-herramienta",
        "lessons": [
            {"title": "La historia de Typhoid Mary — una portadora que no lo sabía", "order": 1, "file": "leccion-01-typhoid-mary.md"},
            {"title": "Tus manos: la técnica que salva vidas", "order": 2, "file": "leccion-02-tus-manos.md"},
            {"title": "Vestimenta, uñas, joyas: lo que sí y lo que no", "order": 3, "file": "leccion-03-vestimenta-y-habitos.md"},
            {"title": "¿Cuándo NO debes trabajar? Enfermedades y heridas", "order": 4, "file": "leccion-04-cuando-no-trabajar.md"},
            {"title": "Tu certificado médico: qué es y por qué importa", "order": 5, "file": "leccion-05-certificado-medico.md"},
        ],
    },
    {
        "title": "La Zona de Peligro",
        "order": 3,
        "dir": "modulo-03-la-zona-de-peligro",
        "lessons": [
            {"title": "El caso Chipotle: contaminación cruzada a gran escala", "order": 1, "file": "leccion-01-caso-chipotle.md"},
            {"title": "¿Qué es la contaminación cruzada? Crudo vs. cocido", "order": 2, "file": "leccion-02-contaminacion-cruzada.md"},
            {"title": "El termómetro es tu mejor amigo: temperaturas de cocción", "order": 3, "file": "leccion-03-temperaturas.md"},
            {"title": "Recibir, guardar y rotar: la regla PEPS", "order": 4, "file": "leccion-04-regla-peps.md"},
            {"title": "La cadena de frío: del proveedor a tu nevera", "order": 5, "file": "leccion-05-cadena-de-frio.md"},
        ],
    },
    {
        "title": "Manos a la Obra",
        "order": 4,
        "dir": "modulo-04-manos-a-la-obra",
        "lessons": [
            {"title": "Limpiar no es desinfectar (y necesitas ambos)", "order": 1, "file": "leccion-01-limpiar-vs-desinfectar.md"},
            {"title": "Tu plan de limpieza: qué, cuándo y con qué", "order": 2, "file": "leccion-02-plan-de-limpieza.md"},
            {"title": "Basuras y residuos: fuera rápido y bien separados", "order": 3, "file": "leccion-03-basuras-y-residuos.md"},
            {"title": "Plagas: si las ves, ya es tarde", "order": 4, "file": "leccion-04-plagas.md"},
        ],
    },
    {
        "title": "Tu Cocina Segura",
        "order": 5,
        "dir": "modulo-05-tu-cocina-segura",
        "lessons": [
            {"title": "Tu día a día: rutina de un manipulador responsable", "order": 1, "file": "leccion-01-rutina-diaria.md"},
            {"title": "¿Qué revisa el inspector del INVIMA?", "order": 2, "file": "leccion-02-visita-invima.md"},
            {"title": "La ley de tu lado: Resolución 2674 en palabras simples", "order": 3, "file": "leccion-03-resolucion-2674-simple.md"},
            {"title": "Repaso y preparación para la evaluación", "order": 4, "file": "leccion-04-repaso-evaluacion.md"},
        ],
    },
]

module_ids: dict[int, str] = {}

for mod in MODULES:
    mod_dir = COURSES_DIR / mod["dir"]
    print(f"\nCreating Module {mod['order']}: {mod['title']}...")
    module = post(f"/companies/{company_id}/education/courses/{course_id}/modules", {
        "title": mod["title"],
        "order": mod["order"],
    })
    mod_id = module["id"]
    module_ids[mod["order"]] = mod_id
    print(f"  Module: {mod_id}")

    for lesson in mod["lessons"]:
        content = read_md(mod_dir / lesson["file"])
        print(f"  Lesson {lesson['order']}: {lesson['title']}")
        les = post(
            f"/companies/{company_id}/education/courses/{course_id}/modules/{mod_id}/lessons",
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
                "is_preview": mod["order"] == 1,  # Module 1 is free preview
            },
        )
        print(f"    -> {les['id']}")

# ---------------------------------------------------------------------------
# 4. Assessment Questions — 25 total (5 per module)
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Creating assessment questions...")
print("=" * 60)

QUESTIONS: list[dict] = [
    # =========================================================================
    # MODULE 1: El Enemigo Invisible (5 questions)
    # =========================================================================

    # Q1 — Scenario: meat delivery
    {
        "text": (
            "Trabajas en la cocina de un restaurante. Al mediodía recibes un pedido "
            "de carne molida. Al tocarla notas que está tibia. El proveedor te dice: "
            "\"Tranquilo, la acabo de sacar del camión.\"\n"
            "\n---\n\n"
            "¿Qué debes hacer?"
        ),
        "question_type": "multiple_choice_single",
        "order": 1,
        "module_order": 1,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Aceptarla y refrigerarla inmediatamente — con frío se arregla", "is_correct": False},
                {"text": "Rechazarla — si está tibia, la cadena de frío se rompió", "is_correct": True},
                {"text": "Aceptarla pero cocinarla de inmediato para matar cualquier bacteria", "is_correct": False},
                {"text": "Olerla y si no huele mal, aceptarla", "is_correct": False},
            ],
        },
    },
    # Q2 — MC: ground meat danger
    {
        "text": "¿Por qué la carne molida es más peligrosa que un filete entero?",
        "question_type": "multiple_choice_single",
        "order": 2,
        "module_order": 1,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Porque tiene más grasa y la grasa atrae más bacterias", "is_correct": False},
                {"text": "Porque al moler la carne, las bacterias de la superficie se mezclan por todo el interior", "is_correct": True},
                {"text": "Porque la carne molida siempre viene de animales más viejos", "is_correct": False},
                {"text": "No es más peligrosa, el riesgo es el mismo", "is_correct": False},
            ],
        },
    },
    # Q3 — True/False: toxins survive heat
    {
        "text": "En una intoxicación alimentaria, calentar la comida a alta temperatura elimina el peligro porque mata tanto la bacteria como la toxina.",
        "question_type": "true_false",
        "order": 3,
        "module_order": 1,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Verdadero", "is_correct": False},
                {"text": "Falso", "is_correct": True},
            ],
        },
    },
    # Q4 — MC: danger zone
    {
        "text": "¿Cuál es el rango de la 'zona de peligro' donde las bacterias se multiplican más rápido?",
        "question_type": "multiple_choice_single",
        "order": 4,
        "module_order": 1,
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
    # Q5 — True/False: gel vs Norovirus
    {
        "text": "El gel antibacterial es suficiente para eliminar el Norovirus de las manos.",
        "question_type": "true_false",
        "order": 5,
        "module_order": 1,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Verdadero", "is_correct": False},
                {"text": "Falso", "is_correct": True},
            ],
        },
    },

    # =========================================================================
    # MODULE 2: Tu Cuerpo, Tu Herramienta (5 questions)
    # =========================================================================

    # Q6 — Scenario: sick coworker
    {
        "text": (
            "Un compañero de la cocina llegó con diarrea. Te dice: \"Ya me tomé una "
            "pastilla, estoy bien. Si me voy me descuentan el día.\"\n"
            "\n---\n\n"
            "¿Qué le dirías?"
        ),
        "question_type": "multiple_choice_single",
        "order": 6,
        "module_order": 2,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Que use doble guante y tapabocas y siga trabajando", "is_correct": False},
                {"text": "Que no toque alimentos listos para consumo pero puede lavar platos", "is_correct": False},
                {"text": "Que debe reportar al supervisor y no manipular alimentos hasta recuperarse", "is_correct": True},
                {"text": "Que se lave bien las manos con gel antibacterial y continúe", "is_correct": False},
            ],
        },
    },
    # Q7 — MC: handwashing time
    {
        "text": "¿Cuánto tiempo mínimo debes frotar tus manos con jabón durante el lavado de manos?",
        "question_type": "multiple_choice_single",
        "order": 7,
        "module_order": 2,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "5 segundos", "is_correct": False},
                {"text": "10 segundos", "is_correct": False},
                {"text": "20 segundos", "is_correct": True},
                {"text": "60 segundos", "is_correct": False},
            ],
        },
    },
    # Q8 — Sorting: handwashing steps
    {
        "text": "Ordena los pasos del lavado de manos correctamente:",
        "question_type": "sorting",
        "order": 8,
        "module_order": 2,
        "config": {
            "type": "sorting",
            "items": [
                "Mojar las manos con agua",
                "Aplicar jabón",
                "Frotar todas las superficies por 20 segundos",
                "Enjuagar con agua corriente",
                "Secar con toalla de papel",
                "Cerrar la llave con la toalla",
            ],
        },
    },
    # Q9 — MC: prohibited items
    {
        "text": "¿Cuál de estos elementos tiene PROHIBIDO portar un manipulador de alimentos durante su jornada?",
        "question_type": "multiple_choice_single",
        "order": 9,
        "module_order": 2,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Gorro o malla para el cabello", "is_correct": False},
                {"text": "Zapatos cerrados antideslizantes", "is_correct": False},
                {"text": "Anillos, pulseras, reloj y aretes", "is_correct": True},
                {"text": "Uniforme de color claro", "is_correct": False},
            ],
        },
    },
    # Q10 — True/False: gloves replace handwashing
    {
        "text": "Usar guantes de látex reemplaza la necesidad de lavarse las manos.",
        "question_type": "true_false",
        "order": 10,
        "module_order": 2,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Verdadero", "is_correct": False},
                {"text": "Falso", "is_correct": True},
            ],
        },
    },

    # =========================================================================
    # MODULE 3: La Zona de Peligro (5 questions)
    # =========================================================================

    # Q11 — Scenario: cross-contamination
    {
        "text": (
            "Estás preparando el almuerzo. Cortaste pollo crudo en la tabla amarilla. "
            "Ahora necesitas picar tomate para la ensalada. Un compañero te dice: "
            "\"Usa la misma tabla, solo límpiala con un trapo húmedo.\"\n"
            "\n---\n\n"
            "¿Es correcto lo que dice tu compañero?"
        ),
        "question_type": "multiple_choice_single",
        "order": 11,
        "module_order": 3,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Sí, limpiar con un trapo húmedo es suficiente", "is_correct": False},
                {"text": "No — debes usar otra tabla o lavar y desinfectar la misma antes de usarla", "is_correct": True},
                {"text": "Sí, si el trapo tiene desinfectante", "is_correct": False},
                {"text": "No importa porque el tomate se va a lavar después", "is_correct": False},
            ],
        },
    },
    # Q12 — Matching: cooking temperatures
    {
        "text": "Relaciona cada alimento con su temperatura mínima de cocción interna:",
        "question_type": "matching",
        "order": 12,
        "module_order": 3,
        "config": {
            "type": "matching",
            "pairs": [
                {"left": "Pollo y aves", "right": "74°C"},
                {"left": "Carne molida", "right": "70°C"},
                {"left": "Pescado", "right": "63°C"},
                {"left": "Cerdo (chuleta, lomo)", "right": "72°C"},
            ],
        },
    },
    # Q13 — MC: fridge organization
    {
        "text": "¿Cuál es la forma correcta de organizar los alimentos en la nevera?",
        "question_type": "multiple_choice_single",
        "order": 13,
        "module_order": 3,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Crudo arriba, cocido abajo — el crudo necesita más frío", "is_correct": False},
                {"text": "Todo junto si está en recipientes cerrados", "is_correct": False},
                {"text": "Cocido arriba, crudo abajo — siempre en recipientes cerrados", "is_correct": True},
                {"text": "No importa el orden si la nevera está a la temperatura correcta", "is_correct": False},
            ],
        },
    },
    # Q14 — MC: PEPS
    {
        "text": "¿Qué significa la regla PEPS y cómo se aplica?",
        "question_type": "multiple_choice_single",
        "order": 14,
        "module_order": 3,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Primero en Entrar, Primero en Salir — los productos más antiguos se usan primero para evitar vencimientos", "is_correct": True},
                {"text": "Primero el Empaque, Primero el Sello — verificar empaques antes de almacenar", "is_correct": False},
                {"text": "Primero en Entrar, Primero en Stock — llenar el inventario antes de vender", "is_correct": False},
                {"text": "Primero en Enfriar, Primero en Servir — lo más frío se sirve primero", "is_correct": False},
            ],
        },
    },
    # Q15 — True/False: refreezing
    {
        "text": "Si un alimento se descongeló completamente, puedes volver a congelarlo sin problema siempre que no huela mal.",
        "question_type": "true_false",
        "order": 15,
        "module_order": 3,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Verdadero", "is_correct": False},
                {"text": "Falso", "is_correct": True},
            ],
        },
    },

    # =========================================================================
    # MODULE 4: Manos a la Obra (5 questions)
    # =========================================================================

    # Q16 — MC: cleaning vs disinfecting
    {
        "text": "¿Cuál es la diferencia entre limpiar y desinfectar?",
        "question_type": "multiple_choice_single",
        "order": 16,
        "module_order": 4,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Son lo mismo — ambos eliminan bacterias", "is_correct": False},
                {"text": "Limpiar quita la suciedad visible; desinfectar elimina los microorganismos. Se necesitan ambos", "is_correct": True},
                {"text": "Desinfectar primero y limpiar después", "is_correct": False},
                {"text": "Solo necesitas desinfectar si la superficie se ve sucia", "is_correct": False},
            ],
        },
    },
    # Q17 — Sorting: cleaning 4 steps
    {
        "text": "Ordena los 4 pasos de limpieza y desinfección de superficies:",
        "question_type": "sorting",
        "order": 17,
        "module_order": 4,
        "config": {
            "type": "sorting",
            "items": [
                "Remover restos de comida",
                "Lavar con detergente/jabón",
                "Enjuagar con agua limpia",
                "Desinfectar con hipoclorito",
            ],
        },
    },
    # Q18 — Classification: hypochlorite concentrations
    {
        "text": "Clasifica cada uso con la concentración correcta de hipoclorito:",
        "question_type": "classification",
        "order": 18,
        "module_order": 4,
        "config": {
            "type": "classification",
            "categories": [
                {"label": "100 ppm"},
                {"label": "200 ppm"},
            ],
            "items": [
                {"text": "Desinfectar frutas y verduras", "correct_category": 0},
                {"text": "Desinfectar mesones y tablas de cortar", "correct_category": 1},
                {"text": "Desinfectar utensilios de cocina", "correct_category": 1},
                {"text": "Desinfectar lechugas para ensalada", "correct_category": 0},
            ],
        },
    },
    # Q19 — Scenario: pest found
    {
        "text": (
            "Al abrir la bodega por la mañana, encuentras pequeños excrementos oscuros "
            "cerca de los sacos de harina. Tu jefe dice: \"Limpia eso rápido y ya, "
            "no es nada.\"\n"
            "\n---\n\n"
            "¿Qué debería hacerse realmente?"
        ),
        "question_type": "multiple_choice_single",
        "order": 19,
        "module_order": 4,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Limpiar y seguir trabajando — solo es un ratón", "is_correct": False},
                {"text": "Comprar veneno para ratones y ponerlo junto a la harina", "is_correct": False},
                {"text": "Aislar los productos afectados, desinfectar el área y llamar a control de plagas", "is_correct": True},
                {"text": "Mover la harina a otro lugar y esperar la fumigación del mes", "is_correct": False},
            ],
        },
    },
    # Q20 — MC: trash management
    {
        "text": "¿Cuál es la forma correcta de manejar las basuras en la cocina?",
        "question_type": "multiple_choice_single",
        "order": 20,
        "module_order": 4,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Sacar la basura solo al final del día para no perder tiempo", "is_correct": False},
                {"text": "Usar canecas sin tapa para que sea más fácil depositar los residuos", "is_correct": False},
                {"text": "Canecas con tapa de pedal, separación por tipo y sacar la basura frecuentemente", "is_correct": True},
                {"text": "Acumular todo en una sola caneca grande para ahorrar bolsas", "is_correct": False},
            ],
        },
    },

    # =========================================================================
    # MODULE 5: Tu Cocina Segura (5 questions)
    # =========================================================================

    # Q21 — Sorting: daily routine order
    {
        "text": "Ordena la rutina diaria correcta de un manipulador al llegar al trabajo:",
        "question_type": "sorting",
        "order": 21,
        "module_order": 5,
        "config": {
            "type": "sorting",
            "items": [
                "Ponerse el uniforme limpio y la malla",
                "Quitarse joyas y accesorios",
                "Lavarse las manos",
                "Inspeccionar nevera y área de trabajo",
                "Preparar solución desinfectante fresca",
            ],
        },
    },
    # Q22 — Classification: inspector areas
    {
        "text": "Clasifica cada hallazgo según el área que revisa el inspector del INVIMA:",
        "question_type": "classification",
        "order": 22,
        "module_order": 5,
        "config": {
            "type": "classification",
            "categories": [
                {"label": "Personal manipulador"},
                {"label": "Condiciones de saneamiento"},
                {"label": "Operación y proceso"},
            ],
            "items": [
                {"text": "Certificado médico vigente", "correct_category": 0},
                {"text": "Plan de limpieza documentado", "correct_category": 1},
                {"text": "Nevera a temperatura correcta", "correct_category": 2},
                {"text": "Uniforme limpio y malla puesta", "correct_category": 0},
                {"text": "Contrato de control de plagas", "correct_category": 1},
                {"text": "Separación de crudo y cocido", "correct_category": 2},
            ],
        },
    },
    # Q23 — MC: Resolución 2674
    {
        "text": "¿Cuál de estos es un DERECHO que te da la Resolución 2674 como manipulador de alimentos?",
        "question_type": "multiple_choice_single",
        "order": 23,
        "module_order": 5,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "El derecho a no usar uniforme si hace mucho calor", "is_correct": False},
                {"text": "El derecho a que tu empleador te capacite y te dé las condiciones adecuadas de trabajo (jabón, uniforme, lavamanos)", "is_correct": True},
                {"text": "El derecho a manipular alimentos estando enfermo si usas guantes", "is_correct": False},
                {"text": "El derecho a no ser inspeccionado si tienes certificado médico", "is_correct": False},
            ],
        },
    },
    # Q24 — Scenario: power outage
    {
        "text": (
            "Hubo un corte de luz de 6 horas en tu restaurante. Al volver la energía, "
            "el termómetro de la nevera marca 18°C. Adentro hay carne cruda, pollo, "
            "queso y salsas preparadas. Tu jefe dice: \"Prende la nevera y en un rato "
            "baja la temperatura.\"\n"
            "\n---\n\n"
            "¿Qué debería hacerse?"
        ),
        "question_type": "multiple_choice_single",
        "order": 24,
        "module_order": 5,
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "Refrigerar todo de nuevo — al bajar la temperatura se arregla", "is_correct": False},
                {"text": "Oler cada producto y descartar solo lo que huela mal", "is_correct": False},
                {"text": "Descartar todos los alimentos perecederos — estuvieron en zona de peligro por horas", "is_correct": True},
                {"text": "Cocinar todo inmediatamente para matar las bacterias", "is_correct": False},
            ],
        },
    },
    # Q25 — Matching: key numbers
    {
        "text": "Relaciona cada dato con su valor correcto:",
        "question_type": "matching",
        "order": 25,
        "module_order": 5,
        "config": {
            "type": "matching",
            "pairs": [
                {"left": "Zona de peligro", "right": "5°C a 60°C"},
                {"left": "Temperatura del pollo cocido", "right": "74°C"},
                {"left": "Temperatura de la nevera", "right": "0°C a 5°C"},
                {"left": "Hipoclorito para superficies", "right": "200 ppm"},
                {"left": "Tiempo de lavado de manos", "right": "20 segundos"},
            ],
        },
    },
    # Q26 — Word Search: key course vocabulary (review activity)
    {
        "text": "Encuentra las 8 palabras clave del curso en la sopa de letras:",
        "question_type": "word_search",
        "order": 26,
        "module_order": 5,
        "config": {
            "type": "word_search",
            "words": ["BACTERIAS", "CRUZADA", "TOXINA", "PLAGAS", "HIGIENE", "NEVERA", "MANOS", "PEPS"],
            "grid_size": 12,
            "grid": [
                ["V", "B", "A", "C", "T", "E", "R", "I", "A", "S", "D", "A"],
                ["I", "H", "H", "E", "D", "X", "S", "C", "T", "N", "N", "H"],
                ["B", "A", "C", "G", "H", "R", "U", "A", "S", "G", "E", "I"],
                ["Z", "V", "Z", "S", "N", "H", "O", "T", "I", "A", "V", "G"],
                ["C", "R", "U", "Z", "A", "D", "A", "F", "Z", "N", "E", "I"],
                ["K", "I", "E", "G", "K", "D", "C", "M", "D", "L", "R", "E"],
                ["L", "U", "I", "T", "O", "X", "I", "N", "A", "B", "A", "N"],
                ["O", "M", "S", "D", "M", "C", "S", "J", "V", "P", "U", "E"],
                ["L", "A", "T", "P", "L", "A", "G", "A", "S", "E", "G", "Z"],
                ["C", "N", "B", "X", "H", "J", "C", "H", "D", "P", "M", "I"],
                ["O", "O", "V", "L", "F", "L", "L", "G", "X", "S", "I", "Z"],
                ["X", "S", "V", "C", "U", "V", "F", "S", "H", "F", "O", "M"],
            ],
            "word_positions": [
                {"word": "BACTERIAS", "row": 0, "col": 1, "direction": "horizontal"},
                {"word": "CRUZADA", "row": 4, "col": 0, "direction": "horizontal"},
                {"word": "TOXINA", "row": 6, "col": 3, "direction": "horizontal"},
                {"word": "PLAGAS", "row": 8, "col": 3, "direction": "horizontal"},
                {"word": "HIGIENE", "row": 1, "col": 11, "direction": "vertical"},
                {"word": "NEVERA", "row": 1, "col": 10, "direction": "vertical"},
                {"word": "MANOS", "row": 7, "col": 1, "direction": "vertical"},
                {"word": "PEPS", "row": 7, "col": 9, "direction": "vertical"},
            ],
        },
    },
]

for q in QUESTIONS:
    mod_order = q.pop("module_order")
    payload = {
        "text": q["text"],
        "question_type": q["question_type"],
        "order": q["order"],
        "module_id": module_ids[mod_order],
        "config": q["config"],
        "randomize": True,
    }
    print(f"  Q{q['order']} (M{mod_order}) [{q['question_type']}]: {q['text'][:55]}...")
    post(
        f"/companies/{company_id}/education/courses/{course_id}/questions",
        payload,
    )

# ---------------------------------------------------------------------------
# 5. Publish the course
# ---------------------------------------------------------------------------

print("\nPublishing course...")
post(f"/companies/{company_id}/education/courses/{course_id}/publish", {})

# ---------------------------------------------------------------------------
# 6. Summary
# ---------------------------------------------------------------------------

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
