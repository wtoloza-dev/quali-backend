"""Seed script: adds word search and crossword activities to modules 4, 5, 6.

Requires the main seed_course.py to have been run first.

Usage:
  python scripts/seed_activities.py
"""

from __future__ import annotations

import random
import string
import sys

import httpx


BASE_URL = "http://localhost:8000/api/v1"
COMPANY_ID = "01KKF8NQXSK4367MVSVZYM9NJ2"
COURSE_ID = "01KKF8NQZN28DWBR9X8HWA89VP"

# Module IDs (from existing seed)
MODULE_4 = "01KKF8NR45MARVYCRKJCQ3JCB8"  # Instalaciones y Equipos
MODULE_5 = "01KKF8NR56DPNSAEEQ48FMNM33"  # Limpieza y Desinfección
MODULE_6 = "01KKF8NR67VRWA4W8M0HPRPZ0F"  # Almacenamiento y Transporte

client = httpx.Client(
    base_url=BASE_URL,
    timeout=30,
    follow_redirects=True,
    headers={"x-dev-seed": "seed-local-dev"},
)


def post(path: str, json: dict) -> dict:
    r = client.post(path, json=json)
    if r.status_code not in (200, 201):
        print(f"ERROR {r.status_code} POST {path}")
        print(r.text)
        sys.exit(1)
    return r.json()


# ── Word search grid generator ─────────────────────────────────────────

DIRECTIONS = [
    ("horizontal", 0, 1),
    ("vertical", 1, 0),
    ("diagonal_down", 1, 1),
]


def generate_word_search(words: list[str], grid_size: int = 12) -> dict:
    """Generate a word search grid with hidden words."""
    grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
    positions: list[dict] = []

    for word in words:
        word_upper = word.upper()
        placed = False
        attempts = 0
        while not placed and attempts < 200:
            attempts += 1
            dir_name, dr, dc = random.choice(DIRECTIONS)
            max_r = grid_size - len(word_upper) * dr if dr else grid_size
            max_c = grid_size - len(word_upper) * dc if dc else grid_size
            if max_r <= 0 or max_c <= 0:
                continue
            r = random.randint(0, max_r - 1)
            c = random.randint(0, max_c - 1)

            # Check if word fits
            can_place = True
            for i, ch in enumerate(word_upper):
                nr, nc = r + i * dr, c + i * dc
                existing = grid[nr][nc]
                if existing != "" and existing != ch:
                    can_place = False
                    break

            if can_place:
                for i, ch in enumerate(word_upper):
                    nr, nc = r + i * dr, c + i * dc
                    grid[nr][nc] = ch
                positions.append({
                    "word": word_upper,
                    "row": r,
                    "col": c,
                    "direction": dir_name,
                })
                placed = True

        if not placed:
            print(f"  WARNING: Could not place word '{word}' in grid")

    # Fill empty cells with random letters
    spanish_letters = string.ascii_uppercase + "ÑÁÉÍÓÚ"
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] == "":
                grid[r][c] = random.choice(spanish_letters)

    return {
        "type": "word_search",
        "words": [w.upper() for w in words],
        "grid_size": grid_size,
        "grid": grid,
        "word_positions": positions,
    }


# ── Seed activities ─────────────────────────────────────────────────────

questions_url = f"/companies/{COMPANY_ID}/education/courses/{COURSE_ID}/questions"

# ── Module 4: Word Search — Instalaciones y Equipos ───────────────────

print("Creating word search for Module 4 (Instalaciones y Equipos)...")
ws4_config = generate_word_search(
    words=["DRENAJE", "VENTILACION", "ACERO", "POTABLE", "PISOS", "FLUJO", "EQUIPO", "SANITARIO"],
    grid_size=14,
)
post(questions_url, {
    "text": "Encuentra las palabras relacionadas con instalaciones y equipos sanitarios en la sopa de letras",
    "question_type": "word_search",
    "config": ws4_config,
    "randomize": False,
    "order": 36,
    "module_id": MODULE_4,
})
print("  Word search created!")

# ── Module 5: Crossword — Limpieza y Desinfección ─────────────────────

print("Creating crossword for Module 5 (Limpieza y Desinfección)...")
cw5_config = {
    "type": "crossword",
    "clues": [
        {
            "number": 1,
            "direction": "across",
            "clue": "Sistema de primeras entradas, primeras salidas (siglas)",
            "answer": "PEPS",
            "row": 0,
            "col": 0,
        },
        {
            "number": 2,
            "direction": "down",
            "clue": "Procedimientos Operativos Estandarizados de Saneamiento (siglas)",
            "answer": "POES",
            "row": 0,
            "col": 0,
        },
        {
            "number": 3,
            "direction": "across",
            "clue": "Proceso que reduce microorganismos a niveles seguros",
            "answer": "DESINFECCION",
            "row": 2,
            "col": 1,
        },
        {
            "number": 4,
            "direction": "down",
            "clue": "Eliminación de suciedad visible de superficies",
            "answer": "LIMPIEZA",
            "row": 0,
            "col": 3,
        },
        {
            "number": 5,
            "direction": "across",
            "clue": "Animales no deseados como roedores e insectos en un establecimiento",
            "answer": "PLAGAS",
            "row": 4,
            "col": 0,
        },
        {
            "number": 6,
            "direction": "down",
            "clue": "Material sólido o líquido que se debe manejar adecuadamente (plural)",
            "answer": "RESIDUOS",
            "row": 4,
            "col": 5,
        },
    ],
    "grid_rows": 12,
    "grid_cols": 13,
}
post(questions_url, {
    "text": "Completa el crucigrama con términos de limpieza, desinfección y control de plagas",
    "question_type": "crossword",
    "config": cw5_config,
    "randomize": False,
    "order": 37,
    "module_id": MODULE_5,
})
print("  Crossword created!")

# ── Module 6: Word Search — Almacenamiento y Transporte ───────────────

print("Creating word search for Module 6 (Almacenamiento y Transporte)...")
ws6_config = generate_word_search(
    words=["CADENA", "FRIO", "ROTULADO", "ETIQUETA", "LOTE", "REGISTRO", "VEHICULO", "PEPS"],
    grid_size=12,
)
post(questions_url, {
    "text": "Encuentra las palabras relacionadas con almacenamiento, transporte y comercialización de alimentos",
    "question_type": "word_search",
    "config": ws6_config,
    "randomize": False,
    "order": 38,
    "module_id": MODULE_6,
})
print("  Word search created!")

print()
print("=" * 60)
print("ACTIVITIES SEED COMPLETE!")
print("  Module 4: Word search (instalaciones)")
print("  Module 5: Crossword (limpieza/desinfección)")
print("  Module 6: Word search (almacenamiento)")
print("=" * 60)
