"""Seed script: creates the 'Manipulación Higiénica de Alimentos' course via the API.

Requirements:
  - The backend must be running at http://localhost:8000
  - Auth must be bypassed (SCOPE=local dev mode)
  - pip install httpx  (or use the project venv)

Usage:
  python scripts/seed_course.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import httpx


BASE_URL = "http://localhost:8000/api/v1"
COURSES_DIR = Path(__file__).resolve().parent.parent.parent / "quali-courses" / "manipulacion-higienica-alimentos"

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
    r = client.post(path, json=json)
    if r.status_code not in (200, 201):
        print(f"ERROR {r.status_code} POST {path}")
        print(r.text)
        sys.exit(1)
    return r.json()


def read_md(filepath: Path) -> str:
    """Read a markdown file and return its content."""
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
        "Curso de formación en manipulación higiénica de alimentos conforme a los "
        "requisitos establecidos en la Resolución 2674 de 2013 del Ministerio de Salud "
        "y Protección Social de Colombia. Al finalizar, el participante estará capacitado "
        "para adoptar las medidas preventivas necesarias para evitar la contaminación o "
        "deterioro de los alimentos, garantizando la inocuidad alimentaria."
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
# 3. Modules and lessons
# ---------------------------------------------------------------------------

MODULES = [
    {
        "title": "Marco Normativo y Conceptos Básicos",
        "order": 1,
        "dir": "modulo-01-marco-normativo",
        "lessons": [
            {"title": "Introducción a la inocuidad alimentaria", "order": 1, "file": "leccion-01-introduccion-inocuidad/contenido.md"},
            {"title": "Resolución 2674 de 2013: alcance y objetivos", "order": 2, "file": "leccion-02-resolucion-2674/contenido.md"},
            {"title": "Definiciones clave: BPM, ETA, contaminación", "order": 3, "file": "leccion-03-definiciones-clave/contenido.md"},
            {"title": "Responsabilidades del manipulador de alimentos", "order": 4, "file": "leccion-04-responsabilidades-manipulador/contenido.md"},
        ],
    },
    {
        "title": "Enfermedades Transmitidas por Alimentos (ETA)",
        "order": 2,
        "dir": "modulo-02-enfermedades-eta",
        "lessons": [
            {"title": "¿Qué son las ETA? Tipos y clasificación", "order": 1, "file": "leccion-01-que-son-eta.md"},
            {"title": "Microorganismos patógenos en alimentos", "order": 2, "file": "leccion-02-microorganismos-patogenos.md"},
            {"title": "Factores que favorecen la contaminación", "order": 3, "file": "leccion-03-factores-contaminacion.md"},
            {"title": "Casos reales y prevención de brotes", "order": 4, "file": "leccion-04-casos-prevencion.md"},
        ],
    },
    {
        "title": "Higiene Personal del Manipulador",
        "order": 3,
        "dir": "modulo-03-higiene-personal",
        "lessons": [
            {"title": "Estado de salud y certificación médica", "order": 1, "file": "leccion-01-estado-salud-certificacion.md"},
            {"title": "Lavado correcto de manos: técnica y frecuencia", "order": 2, "file": "leccion-02-lavado-manos.md"},
            {"title": "Vestimenta y presentación personal", "order": 3, "file": "leccion-03-vestimenta-presentacion.md"},
            {"title": "Hábitos higiénicos y conductas prohibidas", "order": 4, "file": "leccion-04-habitos-higienicos.md"},
        ],
    },
    {
        "title": "Condiciones de Instalaciones y Equipos",
        "order": 4,
        "dir": "modulo-04-instalaciones-equipos",
        "lessons": [
            {"title": "Requisitos de edificaciones e instalaciones", "order": 1, "file": "leccion-01-edificaciones-instalaciones.md"},
            {"title": "Abastecimiento de agua potable e instalaciones sanitarias", "order": 2, "file": "leccion-02-agua-instalaciones-sanitarias.md"},
            {"title": "Equipos y utensilios: diseño y mantenimiento", "order": 3, "file": "leccion-03-equipos-utensilios.md"},
            {"title": "Áreas de trabajo y flujo de procesos", "order": 4, "file": "leccion-04-areas-trabajo-flujo.md"},
        ],
    },
    {
        "title": "Limpieza, Desinfección y Control de Plagas",
        "order": 5,
        "dir": "modulo-05-limpieza-desinfeccion",
        "lessons": [
            {"title": "Principios de limpieza y desinfección", "order": 1, "file": "leccion-01-principios-limpieza.md"},
            {"title": "Programas de saneamiento (POES)", "order": 2, "file": "leccion-02-programas-saneamiento.md"},
            {"title": "Manejo integrado de plagas", "order": 3, "file": "leccion-03-manejo-plagas.md"},
            {"title": "Manejo de residuos sólidos y líquidos", "order": 4, "file": "leccion-04-manejo-residuos.md"},
        ],
    },
    {
        "title": "Almacenamiento, Transporte y Comercialización",
        "order": 6,
        "dir": "modulo-06-almacenamiento-transporte",
        "lessons": [
            {"title": "Recepción y control de materias primas", "order": 1, "file": "leccion-01-recepcion-materias-primas.md"},
            {"title": "Almacenamiento: temperaturas y rotación (PEPS)", "order": 2, "file": "leccion-02-almacenamiento-temperaturas.md"},
            {"title": "Transporte de alimentos: requisitos sanitarios", "order": 3, "file": "leccion-03-transporte-alimentos.md"},
            {"title": "Expendio y comercialización", "order": 4, "file": "leccion-04-expendio-comercializacion.md"},
        ],
    },
]

module_ids: dict[int, str] = {}

for mod in MODULES:
    print(f"Creating module {mod['order']}: {mod['title']}...")
    module = post(f"/companies/{company_id}/education/courses/{course_id}/modules", {
        "title": mod["title"],
        "order": mod["order"],
    })
    mod_id = module["id"]
    module_ids[mod["order"]] = mod_id
    print(f"  Module: {mod_id}")

    for lesson in mod["lessons"]:
        filepath = COURSES_DIR / mod["dir"] / lesson["file"]
        if not filepath.exists():
            print(f"  WARNING: lesson file not found: {filepath}")
            content_body = f"# {lesson['title']}\n\nContenido pendiente."
        else:
            content_body = read_md(filepath)

        print(f"  Creating lesson {lesson['order']}: {lesson['title']}...")
        les = post(
            f"/companies/{company_id}/education/courses/{course_id}/modules/{mod_id}/lessons",
            {
                "title": lesson["title"],
                "content": [
                    {
                        "type": "text",
                        "order": 1,
                        "body": content_body,
                    }
                ],
                "order": lesson["order"],
                "is_preview": mod["order"] == 1,  # all module 1 lessons are free preview
            },
        )
        print(f"    Lesson: {les['id']}")

# ---------------------------------------------------------------------------
# 4. Questions
# ---------------------------------------------------------------------------

print("Creating questions...")

QUESTIONS = [
    # Module 1 — Marco Normativo
    {
        "text": "¿Cuál es la norma colombiana vigente que establece las condiciones sanitarias para la fabricación, procesamiento, preparación, envase, almacenamiento, transporte, distribución y comercialización de alimentos?",
        "question_type": "multiple_choice_single",
        "order": 1,
        "options": [
            {"text": "Decreto 3075 de 1997", "is_correct": False},
            {"text": "Ley 9 de 1979", "is_correct": False},
            {"text": "Resolución 2674 de 2013", "is_correct": True},
            {"text": "Decreto 60 de 2002", "is_correct": False},
        ],
    },
    {
        "text": "Las Buenas Prácticas de Manufactura (BPM) se definen como:",
        "question_type": "multiple_choice_single",
        "order": 2,
        "options": [
            {"text": "Un conjunto de sanciones aplicables a los establecimientos que incumplan la normativa sanitaria", "is_correct": False},
            {"text": "Los principios básicos y prácticas generales de higiene en la manipulación, preparación, elaboración, envasado, almacenamiento, transporte y distribución de alimentos para consumo humano", "is_correct": True},
            {"text": "Un sistema de análisis de peligros exclusivo para la industria farmacéutica", "is_correct": False},
            {"text": "Un programa de capacitación voluntaria para restaurantes de alta categoría", "is_correct": False},
        ],
    },
    {
        "text": "¿Cuál de los siguientes es un ejemplo de contaminación química en alimentos?",
        "question_type": "multiple_choice_single",
        "order": 3,
        "options": [
            {"text": "Presencia de Salmonella en pollo crudo", "is_correct": False},
            {"text": "Hallazgo de un fragmento de vidrio en una ensalada", "is_correct": False},
            {"text": "Residuos de plaguicidas en frutas y verduras", "is_correct": True},
            {"text": "Presencia de un cabello humano en la preparación", "is_correct": False},
        ],
    },
    {
        "text": "Según la Resolución 2674 de 2013, se considera manipulador de alimentos a:",
        "question_type": "multiple_choice_single",
        "order": 4,
        "options": [
            {"text": "Únicamente el chef o cocinero principal de un establecimiento", "is_correct": False},
            {"text": "Solo las personas que cuentan con título profesional en gastronomía", "is_correct": False},
            {"text": "Toda persona que interviene directamente en actividades de fabricación, procesamiento, preparación, envase, almacenamiento, transporte y expendio de alimentos", "is_correct": True},
            {"text": "Exclusivamente el personal que realiza el control de calidad en plantas de producción", "is_correct": False},
        ],
    },
    {
        "text": "Las Enfermedades Transmitidas por Alimentos (ETA) se definen como:",
        "question_type": "multiple_choice_single",
        "order": 5,
        "options": [
            {"text": "Enfermedades causadas exclusivamente por virus presentes en el agua potable", "is_correct": False},
            {"text": "Afecciones respiratorias adquiridas en ambientes de cocina", "is_correct": False},
            {"text": "Alergias alimentarias de origen genético", "is_correct": False},
            {"text": "Enfermedades que se originan por la ingestión de alimentos o agua que contienen agentes contaminantes en cantidades suficientes para afectar la salud", "is_correct": True},
        ],
    },
    # Module 2 — ETA
    {
        "text": "La zona de peligro de temperatura para la proliferación de microorganismos en los alimentos se encuentra entre:",
        "question_type": "multiple_choice_single",
        "order": 6,
        "options": [
            {"text": "0 °C y 25 °C", "is_correct": False},
            {"text": "5 °C y 60 °C", "is_correct": True},
            {"text": "10 °C y 45 °C", "is_correct": False},
            {"text": "-18 °C y 30 °C", "is_correct": False},
        ],
    },
    {
        "text": "La Salmonella es una bacteria que se asocia principalmente con el consumo de:",
        "question_type": "multiple_choice_single",
        "order": 7,
        "options": [
            {"text": "Frutas ácidas como la naranja y el limón", "is_correct": False},
            {"text": "Pan y productos de panadería", "is_correct": False},
            {"text": "Huevos, pollo y carne de cerdo insuficientemente cocidos", "is_correct": True},
            {"text": "Bebidas carbonatadas y jugos pasteurizados", "is_correct": False},
        ],
    },
    {
        "text": "¿Cuál es la diferencia principal entre una infección alimentaria y una intoxicación alimentaria?",
        "question_type": "multiple_choice_single",
        "order": 8,
        "options": [
            {"text": "La infección es más grave que la intoxicación", "is_correct": False},
            {"text": "En la infección el microorganismo vivo causa la enfermedad, mientras que en la intoxicación la enfermedad es causada por las toxinas producidas por el microorganismo", "is_correct": True},
            {"text": "La intoxicación solo ocurre con alimentos de origen vegetal y la infección con alimentos de origen animal", "is_correct": False},
            {"text": "No existe diferencia; ambos términos son sinónimos", "is_correct": False},
        ],
    },
    {
        "text": "Según la Organización Mundial de la Salud (OMS), ¿cuál de las siguientes es una de las cinco claves para la inocuidad de los alimentos?",
        "question_type": "multiple_choice_single",
        "order": 9,
        "options": [
            {"text": "Utilizar guantes de látex en todo momento", "is_correct": False},
            {"text": "Consumir los alimentos en un plazo máximo de dos horas", "is_correct": False},
            {"text": "Separar alimentos crudos de los cocidos", "is_correct": True},
            {"text": "Refrigerar todos los alimentos a -18 °C", "is_correct": False},
        ],
    },
    {
        "text": "La contaminación cruzada se produce cuando:",
        "question_type": "multiple_choice_single",
        "order": 10,
        "options": [
            {"text": "Un alimento se cocina a temperatura insuficiente", "is_correct": False},
            {"text": "Se utiliza agua no potable para el lavado de frutas", "is_correct": False},
            {"text": "Microorganismos o sustancias contaminantes se transfieren de un alimento o superficie a otro, por ejemplo al usar la misma tabla para cortar pollo crudo y ensalada", "is_correct": True},
            {"text": "Un alimento permanece más de 24 horas fuera de refrigeración", "is_correct": False},
        ],
    },
    # Module 3 — Higiene Personal
    {
        "text": "Según la técnica de lavado de manos recomendada por la OMS, ¿cuánto tiempo debe durar el procedimiento completo?",
        "question_type": "multiple_choice_single",
        "order": 11,
        "options": [
            {"text": "Al menos 20 segundos", "is_correct": False},
            {"text": "10 segundos son suficientes si se usa jabón antibacterial", "is_correct": False},
            {"text": "De 40 a 60 segundos", "is_correct": True},
            {"text": "Al menos 2 minutos", "is_correct": False},
        ],
    },
    {
        "text": "¿Cuál de los siguientes elementos tiene PROHIBIDO portar un manipulador de alimentos durante su jornada laboral?",
        "question_type": "multiple_choice_single",
        "order": 12,
        "options": [
            {"text": "Gorro o cofia", "is_correct": False},
            {"text": "Tapabocas desechable", "is_correct": False},
            {"text": "Calzado cerrado antideslizante", "is_correct": False},
            {"text": "Anillos, pulseras, reloj y aretes", "is_correct": True},
        ],
    },
    {
        "text": "¿En cuál de las siguientes situaciones es OBLIGATORIO lavarse las manos?",
        "question_type": "multiple_choice_single",
        "order": 13,
        "options": [
            {"text": "Únicamente al iniciar la jornada laboral", "is_correct": False},
            {"text": "Solo después de ir al baño", "is_correct": False},
            {"text": "Después de ir al baño, después de manipular alimentos crudos, después de tocar basura, después de estornudar o toser, y antes de manipular alimentos listos para consumo", "is_correct": True},
            {"text": "Solo cuando las manos se ven visiblemente sucias", "is_correct": False},
        ],
    },
    {
        "text": "Respecto al uniforme del manipulador de alimentos, ¿cuál de las siguientes afirmaciones es correcta?",
        "question_type": "multiple_choice_single",
        "order": 14,
        "options": [
            {"text": "El uniforme puede ser del color que el manipulador prefiera, incluyendo ropa de calle", "is_correct": False},
            {"text": "Solo es obligatorio usar gorro; el resto de la vestimenta es opcional", "is_correct": False},
            {"text": "Debe ser de color claro, estar limpio, usarse exclusivamente en el área de trabajo, e incluir gorro que cubra todo el cabello, tapabocas y calzado cerrado", "is_correct": True},
            {"text": "El uniforme es obligatorio solo para el personal que trabaja en plantas industriales", "is_correct": False},
        ],
    },
    {
        "text": "Cuando un manipulador de alimentos presenta síntomas de enfermedad gastrointestinal (diarrea, vómito, fiebre), ¿qué debe hacer?",
        "question_type": "multiple_choice_single",
        "order": 15,
        "options": [
            {"text": "Continuar trabajando normalmente pero usando doble guante", "is_correct": False},
            {"text": "Tomar medicamento y seguir con sus funciones", "is_correct": False},
            {"text": "Reportar su estado de salud al supervisor y ser retirado de las áreas de manipulación de alimentos hasta que se recupere", "is_correct": True},
            {"text": "Usar tapabocas adicional y evitar tocar alimentos con las manos", "is_correct": False},
        ],
    },
    # Module 4 — Instalaciones y Equipos
    {
        "text": "Según la normativa sanitaria, los pisos de las áreas de procesamiento de alimentos deben ser:",
        "question_type": "multiple_choice_single",
        "order": 16,
        "options": [
            {"text": "De madera tratada para facilitar la limpieza", "is_correct": False},
            {"text": "De material resistente, no absorbente, lavable, antideslizante y con la inclinación adecuada para facilitar el drenaje", "is_correct": True},
            {"text": "Cubiertos con alfombra industrial para evitar accidentes", "is_correct": False},
            {"text": "De cualquier material siempre que se trapeen diariamente", "is_correct": False},
        ],
    },
    {
        "text": "¿Cuál es el requisito fundamental del agua utilizada en un establecimiento donde se manipulan alimentos?",
        "question_type": "multiple_choice_single",
        "order": 17,
        "options": [
            {"text": "Debe estar filtrada pero no necesariamente tratada", "is_correct": False},
            {"text": "Debe ser agua potable, cumplir con la normativa vigente de calidad del agua y contar con registros que demuestren su potabilidad", "is_correct": True},
            {"text": "Basta con que sea agua de acueducto, sin necesidad de verificar su calidad", "is_correct": False},
            {"text": "Solo el agua que entra en contacto directo con los alimentos debe ser potable", "is_correct": False},
        ],
    },
    {
        "text": "¿Por qué se recomienda el acero inoxidable como material principal para equipos y utensilios en contacto con alimentos?",
        "question_type": "multiple_choice_single",
        "order": 18,
        "options": [
            {"text": "Porque es el material más económico del mercado", "is_correct": False},
            {"text": "Porque le da mejor sabor a los alimentos", "is_correct": False},
            {"text": "Porque es resistente a la corrosión, no es tóxico, no absorbente, es fácil de limpiar y desinfectar, y no transfiere sustancias al alimento", "is_correct": True},
            {"text": "Porque es obligatorio por ley usar únicamente este material", "is_correct": False},
        ],
    },
    {
        "text": "La separación de áreas en un establecimiento de alimentos (recepción, almacenamiento, preparación, servicio) tiene como objetivo principal:",
        "question_type": "multiple_choice_single",
        "order": 19,
        "options": [
            {"text": "Mejorar la apariencia estética del establecimiento", "is_correct": False},
            {"text": "Prevenir la contaminación cruzada y mantener el flujo adecuado del proceso desde la materia prima hasta el producto terminado", "is_correct": True},
            {"text": "Cumplir un requisito arquitectónico sin relación con la inocuidad", "is_correct": False},
            {"text": "Facilitar la supervisión de los empleados por parte del administrador", "is_correct": False},
        ],
    },
    {
        "text": "¿Cuál es la función principal de una ventilación adecuada en las áreas de procesamiento de alimentos?",
        "question_type": "multiple_choice_single",
        "order": 20,
        "options": [
            {"text": "Mantener una temperatura agradable para los trabajadores exclusivamente", "is_correct": False},
            {"text": "Eliminar por completo los microorganismos del ambiente", "is_correct": False},
            {"text": "Evitar la acumulación de calor, humedad, humo y vapores que puedan favorecer la condensación y el crecimiento microbiano, y garantizar la renovación del aire", "is_correct": True},
            {"text": "Cumplir con normas laborales que no tienen relación con la inocuidad alimentaria", "is_correct": False},
        ],
    },
    # Module 5 — Limpieza y Desinfección
    {
        "text": "¿Cuál es la diferencia entre limpieza y desinfección?",
        "question_type": "multiple_choice_single",
        "order": 21,
        "options": [
            {"text": "Son el mismo proceso; ambos términos se usan indistintamente", "is_correct": False},
            {"text": "La limpieza elimina microorganismos y la desinfección elimina suciedad visible", "is_correct": False},
            {"text": "La limpieza elimina la suciedad visible (restos de alimentos, grasa) y la desinfección reduce los microorganismos a niveles seguros mediante agentes químicos o físicos", "is_correct": True},
            {"text": "La desinfección se hace solo con agua caliente y la limpieza solo con jabón", "is_correct": False},
        ],
    },
    {
        "text": "Los Procedimientos Operativos Estandarizados de Saneamiento (POES) son:",
        "question_type": "multiple_choice_single",
        "order": 22,
        "options": [
            {"text": "Recetas estandarizadas de cocina para garantizar la calidad del producto", "is_correct": False},
            {"text": "Documentos escritos que describen de manera detallada los procedimientos de limpieza y desinfección que se deben realizar antes, durante y después de las operaciones, incluyendo frecuencia, responsables, productos y concentraciones", "is_correct": True},
            {"text": "Informes mensuales de ventas que debe presentar todo establecimiento de alimentos", "is_correct": False},
            {"text": "Manuales exclusivos para empresas con más de 50 empleados", "is_correct": False},
        ],
    },
    {
        "text": "En un programa de control integrado de plagas, ¿cuál de las siguientes medidas se considera de primera línea?",
        "question_type": "multiple_choice_single",
        "order": 23,
        "options": [
            {"text": "Aplicar insecticidas de manera continua y preventiva en todas las áreas", "is_correct": False},
            {"text": "Implementar medidas preventivas como sellar grietas, instalar anjeos en ventanas, mantener limpieza permanente y manejar adecuadamente los residuos para evitar el ingreso y proliferación de plagas", "is_correct": True},
            {"text": "Colocar veneno para roedores dentro de las áreas de preparación de alimentos", "is_correct": False},
            {"text": "Fumigar exclusivamente cuando haya presencia visible de plagas", "is_correct": False},
        ],
    },
    {
        "text": "El manejo adecuado de residuos sólidos en un establecimiento de alimentos incluye:",
        "question_type": "multiple_choice_single",
        "order": 24,
        "options": [
            {"text": "Acumular las basuras en bolsas abiertas al lado de la zona de preparación para mayor comodidad", "is_correct": False},
            {"text": "Retirar los residuos únicamente al final de la jornada laboral", "is_correct": False},
            {"text": "Clasificar los residuos, depositarlos en recipientes con tapa de accionamiento no manual, retirarlos frecuentemente del área de producción y almacenarlos en un área separada y cubierta hasta su recolección final", "is_correct": True},
            {"text": "Quemar los residuos orgánicos en el patio trasero del establecimiento", "is_correct": False},
        ],
    },
    {
        "text": "¿Por qué es importante respetar el tiempo de contacto indicado en la ficha técnica de un desinfectante?",
        "question_type": "multiple_choice_single",
        "order": 25,
        "options": [
            {"text": "Porque un menor tiempo de contacto hace que el desinfectante sea más potente", "is_correct": False},
            {"text": "No es importante; basta con aplicar el producto y enjuagar inmediatamente", "is_correct": False},
            {"text": "Solo es importante cuando se desinfectan baños, no superficies de alimentos", "is_correct": False},
            {"text": "Porque el desinfectante necesita un tiempo mínimo de exposición con la superficie para lograr la reducción efectiva de los microorganismos a niveles seguros", "is_correct": True},
        ],
    },
    # Module 6 — Almacenamiento y Transporte
    {
        "text": "El sistema PEPS (Primeras Entradas, Primeras Salidas), también conocido como FIFO, consiste en:",
        "question_type": "multiple_choice_single",
        "order": 26,
        "options": [
            {"text": "Utilizar primero los productos que ingresaron primero al almacén, rotando el inventario según la fecha de recepción o vencimiento para evitar que los alimentos se venzan o deterioren", "is_correct": True},
            {"text": "Almacenar los productos más pesados en los estantes superiores y los más livianos abajo", "is_correct": False},
            {"text": "Despachar primero los productos más costosos para recuperar la inversión", "is_correct": False},
            {"text": "Organizar los alimentos por orden alfabético en la bodega", "is_correct": False},
        ],
    },
    {
        "text": "¿A qué temperatura deben mantenerse los alimentos congelados para garantizar su conservación adecuada?",
        "question_type": "multiple_choice_single",
        "order": 27,
        "options": [
            {"text": "A 0 °C", "is_correct": False},
            {"text": "Entre -5 °C y -10 °C", "is_correct": False},
            {"text": "A -18 °C o inferior", "is_correct": True},
            {"text": "Entre -1 °C y -5 °C", "is_correct": False},
        ],
    },
    {
        "text": "¿Cuál es el rango de temperatura adecuado para la refrigeración de alimentos perecederos?",
        "question_type": "multiple_choice_single",
        "order": 28,
        "options": [
            {"text": "Entre 0 °C y 4 °C", "is_correct": True},
            {"text": "Entre 0 °C y 5 °C", "is_correct": False},
            {"text": "Entre 0 °C y 8 °C", "is_correct": False},
            {"text": "Entre -5 °C y 0 °C", "is_correct": False},
        ],
    },
    {
        "text": "¿Cuál de las siguientes condiciones debe cumplir el vehículo utilizado para el transporte de alimentos perecederos?",
        "question_type": "multiple_choice_single",
        "order": 29,
        "options": [
            {"text": "Puede ser cualquier vehículo siempre que esté limpio por fuera", "is_correct": False},
            {"text": "Solo necesita un compartimento cerrado si el trayecto supera las dos horas", "is_correct": False},
            {"text": "Debe contar con unidad de refrigeración que mantenga la cadena de frío, ser de material sanitario lavable, estar en buenas condiciones de higiene y ser de uso exclusivo para el transporte de alimentos", "is_correct": True},
            {"text": "Basta con cubrir los alimentos con una lona plástica durante el transporte", "is_correct": False},
        ],
    },
    {
        "text": "¿Qué información mínima debe contener la etiqueta o rotulado de un alimento envasado según la normativa colombiana?",
        "question_type": "multiple_choice_single",
        "order": 30,
        "options": [
            {"text": "Solo el nombre del producto y la fecha de vencimiento", "is_correct": False},
            {"text": "Únicamente el precio de venta al público y el código de barras", "is_correct": False},
            {"text": "Nombre del producto, lista de ingredientes, contenido neto, nombre y dirección del fabricante, lote, fecha de vencimiento, registro sanitario y condiciones de conservación", "is_correct": True},
            {"text": "Solo el nombre del fabricante y el número de teléfono de atención al cliente", "is_correct": False},
        ],
    },
    # Practical scenarios
    {
        "text": "Un manipulador de alimentos se corta un dedo mientras pica verduras. La herida es pequeña pero sangra. ¿Cuál es la acción correcta?",
        "question_type": "multiple_choice_single",
        "order": 31,
        "options": [
            {"text": "Lavar la herida con agua, cubrirla con una curita convencional y continuar trabajando", "is_correct": False},
            {"text": "Ignorar la herida si deja de sangrar y seguir manipulando alimentos", "is_correct": False},
            {"text": "Lavar y desinfectar la herida, cubrirla con un vendaje impermeable de color visible (preferiblemente azul), colocar un guante sobre el vendaje y, si la herida impide la manipulación segura, reasignar al trabajador a tareas sin contacto directo con alimentos", "is_correct": True},
            {"text": "Aplicar alcohol directamente sobre el alimento que se estaba cortando para desinfectarlo y continuar la preparación", "is_correct": False},
        ],
    },
    {
        "text": "Al recibir un pedido de pechugas de pollo refrigeradas, usted verifica con el termómetro que el producto llega a 12 °C. El transportador le indica que el camión tuvo una falla en la refrigeración durante el trayecto. ¿Qué debe hacer?",
        "question_type": "multiple_choice_single",
        "order": 32,
        "options": [
            {"text": "Aceptar el pedido y refrigerarlo inmediatamente para que baje la temperatura", "is_correct": False},
            {"text": "Aceptar el pedido solo si el producto no presenta mal olor", "is_correct": False},
            {"text": "Aceptar el pedido con un descuento por la condición de temperatura", "is_correct": False},
            {"text": "Rechazar el pedido, registrar la novedad en el formato de recepción de materias primas indicando la ruptura de la cadena de frío, y notificar al proveedor", "is_correct": True},
        ],
    },
    {
        "text": "En una cocina, un auxiliar utiliza la misma tabla de corte y el mismo cuchillo para filetear pollo crudo y luego, sin lavar los utensilios, procede a picar tomate para una ensalada que se servirá sin cocción. ¿Cuál es el error y el riesgo asociado?",
        "question_type": "multiple_choice_single",
        "order": 33,
        "options": [
            {"text": "El error es no usar guantes; el riesgo es una contaminación física", "is_correct": False},
            {"text": "No hay error significativo si el pollo estaba refrigerado correctamente", "is_correct": False},
            {"text": "El error es no lavar y desinfectar la tabla y el cuchillo (o usar utensilios exclusivos para cada tipo de alimento); el riesgo es contaminación cruzada que puede transferir bacterias como Salmonella del pollo crudo a la ensalada lista para consumo", "is_correct": True},
            {"text": "El error es picar el tomate después del pollo; lo correcto es picar siempre primero las verduras, sin necesidad de lavar los utensilios entre usos", "is_correct": False},
        ],
    },
    {
        "text": "Durante una inspección matutina del área de almacenamiento, usted descubre excrementos de roedores cerca de los estantes donde se almacenan granos y harinas. ¿Cuál es la acción prioritaria?",
        "question_type": "multiple_choice_single",
        "order": 34,
        "options": [
            {"text": "Limpiar los excrementos y continuar con las operaciones normales", "is_correct": False},
            {"text": "Colocar veneno para roedores junto a los alimentos para eliminar la plaga rápidamente", "is_correct": False},
            {"text": "Aislar y evaluar los productos que pudieron estar en contacto con los excrementos para su descarte, limpiar y desinfectar el área, reportar la situación para que se apliquen medidas de control integrado de plagas y se identifiquen los puntos de ingreso", "is_correct": True},
            {"text": "Mover los alimentos a otra área y esperar a la fumigación mensual programada", "is_correct": False},
        ],
    },
    {
        "text": "En un restaurante se produce un corte de energía eléctrica que dura 6 horas. Al restablecerse el servicio, el termómetro del refrigerador marca 18 °C. Dentro hay carnes crudas, lácteos y salsas preparadas. ¿Cuál es la decisión correcta?",
        "question_type": "multiple_choice_single",
        "order": 35,
        "options": [
            {"text": "Volver a refrigerar todos los productos; al bajar la temperatura serán seguros nuevamente", "is_correct": False},
            {"text": "Oler y probar los alimentos para verificar si todavía están en buen estado antes de decidir", "is_correct": False},
            {"text": "Cocinar inmediatamente todas las carnes para aprovecharlas y solo descartar los lácteos", "is_correct": False},
            {"text": "Descartar todos los alimentos perecederos que superaron los 5 °C durante un tiempo prolongado, ya que permanecieron en la zona de peligro de temperatura y pueden haber desarrollado niveles inseguros de microorganismos, aunque no presenten cambios visibles ni de olor", "is_correct": True},
        ],
    },
]

# Map question order ranges to module orders:
# 1-5 → Module 1, 6-10 → Module 2, ..., 26-30 → Module 6, 31-35 → Module 6 (practical)
def question_module_order(q_order: int) -> int:
    if q_order <= 30:
        return ((q_order - 1) // 5) + 1
    return 6  # practical scenarios go to module 6


for q in QUESTIONS:
    mod_order = question_module_order(q["order"])
    # Move top-level options into config for the unified schema
    options = q.pop("options", [])
    q_payload = {
        **q,
        "module_id": module_ids[mod_order],
        "config": {"type": "multiple_choice", "options": options},
    }
    print(f"  Q{q['order']} (mod {mod_order}): {q['text'][:60]}...")
    post(f"/companies/{company_id}/education/courses/{course_id}/questions", q_payload)

# ---------------------------------------------------------------------------
# 5. Publish course
# ---------------------------------------------------------------------------

print("Publishing course...")
post(f"/companies/{company_id}/education/courses/{course_id}/publish", {})

print()
print("=" * 60)
print("SEED COMPLETE!")
print(f"  Company ID: {company_id}")
print(f"  Course ID:  {course_id}")
print("  Status:     published")
print("=" * 60)
