#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Genera dos archivos Markdown en el directorio actual:
1. README.md  → con resúmenes generados por Ollama (si disponible)
2. diario.md  → misma jerarquía pero sin resúmenes, solo fechas
Estructura esperada: UNIDAD / SUBUNIDAD / 101-Ejercicios / archivos
"""

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess
import shutil
import re
import os

# ===================== Configuración =====================
BASE_PATH = Path(os.getcwd())               # Usa el directorio actual
OUTPUT_FILE = BASE_PATH / "README.md"
OUTPUT_FILE_DIARIO = BASE_PATH / "diario.md"
EXCLUDE_DIRS = {".git", ".vscode"}
TARGET_SUBFOLDER = "101-Ejercicios"
TZ = ZoneInfo("Europe/Madrid")

OLLAMA_MODEL = "llama3.1:8b-instruct-q4_0"  # o 'qwen2.5-coder:7b'

# Límites de seguridad
MAX_SUBUNIT_PROMPT_CHARS = 20000
PER_FILE_SNIPPET_CHARS   = 2500
MAX_FILES_PER_SUBUNIT    = 40
MAX_FILE_SIZE_BYTES      = 2 * 1024 * 1024

# Longitud objetivo del párrafo final
MAX_SUMMARY_WORDS = 160
MAX_SENTENCES = 6
# =========================================================


def human_date(ts: float) -> str:
    return datetime.fromtimestamp(ts, TZ).strftime("%Y-%m-%d")


def file_birth_or_mtime(p: Path) -> float:
    st = p.stat()
    return getattr(st, "st_birthtime", st.st_mtime)


def list_dir_clean(p: Path):
    if not p.is_dir():
        return []
    for child in sorted(p.iterdir(), key=lambda x: x.name.lower()):
        if child.name in EXCLUDE_DIRS:
            continue
        yield child


def is_text_file(path: Path) -> bool:
    try:
        if not path.is_file():
            return False
        size = path.stat().st_size
        if size == 0 or size > MAX_FILE_SIZE_BYTES:
            return False
        with path.open("rb") as fh:
            head = fh.read(4096)
        if b"\x00" in head:
            return False
        head.decode("utf-8", errors="ignore")
        return True
    except Exception:
        return False


def safe_read_text(path: Path, limit: int = PER_FILE_SNIPPET_CHARS) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    if len(data) <= limit:
        return data
    chunk = max(1, limit // 3)
    start = data[:chunk]
    mid_start = max((len(data) - chunk) // 2, 0)
    middle = data[mid_start: mid_start + chunk]
    end = data[-chunk:]
    return f"{start}\n...\n{middle}\n...\n{end}"


def summarize_dates(folder: Path):
    if not (folder.exists() and folder.is_dir()):
        return None
    files = [f for f in folder.iterdir() if f.is_file()]
    if not files:
        return None
    times = [file_birth_or_mtime(f) for f in files]
    return min(times), max(times)


def build_ollama_prompt(subunit_name: str, file_snippets: list[str]) -> str:
    guardrails = (
        f"Instrucciones (OBLIGATORIAS):\n"
        f"- Redacta exactamente UN párrafo en español, 3–6 frases, ~90–140 palabras, "
        f"que resuma lo ENSEÑADO en la clase correspondiente a la subunidad «{subunit_name}».\n"
        f"- Prohibido encabezados, listas, viñetas, enumeraciones o bloques de código.\n"
        f"- Prohibido prefacios o frases metadiscursivas.\n"
        f"- Prohibido consejos, sugerencias o evaluaciones.\n"
        f"- No describas funciones ni pasos concretos; sintetiza conceptos y prácticas.\n"
        f"- Devuelve ÚNICAMENTE el párrafo final, sin comillas ni título.\n\n"
        f"Fragmentos de archivos de la subunidad:\n\n"
    )
    body = "\n\n".join(file_snippets)
    return (guardrails + body)[:MAX_SUBUNIT_PROMPT_CHARS]


def run_ollama(model: str, prompt: str) -> str | None:
    if shutil.which("ollama") is None:
        return None
    try:
        proc = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            check=False,
            timeout=3600
        )
        out = (proc.stdout or "").strip()
        return out if out else None
    except Exception:
        return None


INTRO_PATTERNS = [
    r"^\s*aqu[ií] te presento.*?$",
    r"^\s*en (esta|la) (secci[oó]n|subunidad).*?$",
    r"^\s*a continuaci[oó]n.*?$",
    r"^\s*este (documento|c[oó]digo|m[oó]dulo).*?$",
    r"^\s*el c[oó]digo proporcionado.*?$",
    r"^\s*en general,.*?$",
    r"^\s*resumen:?\s*",
]
ADVICE_PATTERNS = [
    r"\b(te\s+recomiendo|recomendamos|recomendar[ií]a|deber[ií]as|debes|conviene|"
    r"sugerimos|sugerenc[ií]a|considera|puedes|recuerda|es importante|"
    r"te proporcionar[eé]|te dar[eé]|te indicar[eé])\b"
]
INTRO_REGEXES = [re.compile(pat, re.IGNORECASE | re.MULTILINE) for pat in INTRO_PATTERNS]
ADVICE_REGEXES = [re.compile(pat, re.IGNORECASE) for pat in ADVICE_PATTERNS]
SENTENCE_SPLIT = re.compile(r"(?<=[\.\?\!])\s+")


def clean_to_single_paragraph(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"^\s*#{1,6}\s+.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*•]\s+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[\.)]\s+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip(" \t\r\n-—:;")
    for rx in ADVICE_REGEXES + INTRO_REGEXES:
        text = rx.sub("", text)
    sentences = SENTENCE_SPLIT.split(text)
    text = " ".join(sentences[:MAX_SENTENCES])
    words = text.split()
    if len(words) > MAX_SUMMARY_WORDS:
        text = " ".join(words[:MAX_SUMMARY_WORDS]).rstrip(",.;:") + "."
    return text.strip()


# -------------------- Informe con resúmenes --------------------

def build_report_units(base: Path) -> str:
    lines = [
        "# Informe de 101-Ejercicios (Unidad/Subunidad)",
        "",
        f"_Base:_ `{base}`",
        f"_Generado:_ {human_date(datetime.now(TZ).timestamp())}",
        f"_Modelo Ollama:_ `{OLLAMA_MODEL}`",
        ""
    ]

    any_unit = False

    for unidad in list_dir_clean(base):
        if not unidad.is_dir():
            continue
        unit_lines, unit_has = [f"## Unidad: `{unidad.name}`"], False

        for subunidad in list_dir_clean(unidad):
            if not subunidad.is_dir():
                continue

            ejercicios_dir = subunidad / TARGET_SUBFOLDER
            resumen_fechas = summarize_dates(ejercicios_dir)
            if not resumen_fechas:
                continue

            text_files = [
                f for f in sorted(ejercicios_dir.iterdir(), key=lambda x: x.name.lower())
                if is_text_file(f)
            ]
            if not text_files:
                continue

            snippets, total_chars = [], 0
            for f in text_files[:MAX_FILES_PER_SUBUNIT]:
                snippet = f"### {f.name}\n{safe_read_text(f)}"
                if total_chars + len(snippet) > MAX_SUBUNIT_PROMPT_CHARS:
                    break
                snippets.append(snippet)
                total_chars += len(snippet)

            earliest, latest = resumen_fechas
            d1, d2 = human_date(earliest), human_date(latest)
            date_str = d1 if d1 == d2 else f"{d1} → {d2}"

            prompt = build_ollama_prompt(subunidad.name, snippets)
            raw_summary = run_ollama(OLLAMA_MODEL, prompt)
            summary = clean_to_single_paragraph(raw_summary or "")

            unit_lines.append(f"- `{subunidad.name}` — {date_str}")
            unit_lines.append(f"  - **Resumen:** {summary or '_No disponible_'}")
            unit_has = True

        if unit_has:
            lines.extend(unit_lines + [""])
            any_unit = True

    if not any_unit:
        lines.append("_No se encontraron subunidades con archivos de texto en `101-Ejercicios`._\n")
    return "\n".join(lines)


# -------------------- Diario sin resúmenes --------------------

def build_diario_units(base: Path) -> str:
    lines = [
        "# Diario de 101-Ejercicios (Unidad/Subunidad)",
        "",
        f"_Base:_ `{base}`",
        f"_Generado:_ {human_date(datetime.now(TZ).timestamp())}",
        ""
    ]

    any_unit = False

    for unidad in list_dir_clean(base):
        if not unidad.is_dir():
            continue
        unit_lines, unit_has = [f"## Unidad: `{unidad.name}`"], False

        for subunidad in list_dir_clean(unidad):
            if not subunidad.is_dir():
                continue

            ejercicios_dir = subunidad / TARGET_SUBFOLDER
            resumen_fechas = summarize_dates(ejercicios_dir)
            if not resumen_fechas:
                continue

            text_files = [
                f for f in sorted(ejercicios_dir.iterdir(), key=lambda x: x.name.lower())
                if is_text_file(f)
            ]
            if not text_files:
                continue

            earliest, latest = resumen_fechas
            d1, d2 = human_date(earliest), human_date(latest)
            date_str = d1 if d1 == d2 else f"{d1} → {d2}"

            unit_lines.append(f"- `{subunidad.name}` — {date_str}")
            unit_has = True

        if unit_has:
            lines.extend(unit_lines + [""])
            any_unit = True

    if not any_unit:
        lines.append("_No se encontraron subunidades con archivos de texto en `101-Ejercicios`._\n")
    return "\n".join(lines)


# -------------------- Main --------------------

if __name__ == "__main__":
    report = build_report_units(BASE_PATH)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"✅ Informe generado: {OUTPUT_FILE}")

    diario = build_diario_units(BASE_PATH)
    OUTPUT_FILE_DIARIO.write_text(diario, encoding="utf-8")
    print(f"✅ Diario generado: {OUTPUT_FILE_DIARIO}")

