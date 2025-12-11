#!/usr/bin/env python3
import os
import re
from pathlib import Path

# -----------------------------
# Utilidades de ordenación y nombres
# -----------------------------

def sort_key(entry: os.DirEntry):
    name = entry.name
    m = re.match(r"^(\d+)[\s\-_.]?(.*)", name)
    if m:
        num = int(m.group(1))
        rest = m.group(2).strip().lower()
        return (num, rest)
    return (9999, name.lower())


def title_from_name(name: str) -> str:
    m = re.match(r"^(\d+)[\s\-_.]?(.*)", name)
    if m:
        title = m.group(2).strip()
        if title:
            return title
    return name


def language_from_extension(path: Path) -> str:
    ext = path.suffix.lower()
    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".md": "markdown",
        ".sh": "bash",
        ".sql": "sql",
        ".xml": "xml",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".txt": "",
    }
    return mapping.get(ext, "")

# -----------------------------
# Detección de TEXTO vs BINARIO
# -----------------------------

def is_text_file(path: Path, blocksize: int = 4096) -> bool:
    """
    Devuelve True si el archivo parece ser de texto.
    Para determinarlo, lee un bloque del archivo en binario y comprueba si hay bytes nulos.
    """
    try:
        with path.open("rb") as f:
            chunk = f.read(blocksize)
        if b"\0" in chunk:
            return False
        return True
    except Exception:
        return False


# -----------------------------
# Lógica principal
# -----------------------------

def main(root_dir: Path):
    output_path = root_dir / "apuntes.md"
    lines = []

    units = [e for e in os.scandir(root_dir) if e.is_dir()]
    units.sort(key=sort_key)

    for unit in units:
        unit_title = title_from_name(unit.name)
        lines.append(f"# {unit_title}")
        lines.append("")

        subunits = [e for e in os.scandir(unit.path) if e.is_dir()]
        subunits.sort(key=sort_key)

        for subunit in subunits:
            sub_title = title_from_name(subunit.name)
            lines.append(f"## {sub_title}")
            lines.append("")

            subunit_path = Path(subunit.path)

            # ------- CONTENIDOS BÁSICOS -------
            contenidos_folder = None
            for e in os.scandir(subunit_path):
                if e.is_dir() and e.name.lower().startswith("001-contenidos"):
                    contenidos_folder = Path(e.path)
                    break

            if contenidos_folder and contenidos_folder.exists():
                md_files = [
                    Path(f.path) for f in os.scandir(contenidos_folder)
                    if f.is_file() and f.name.lower().endswith((".md", ".markdown"))
                ]
                md_files.sort(key=lambda p: p.name.lower())
                for md_file in md_files:
                    with md_file.open("r", encoding="utf-8") as f:
                        content = f.read().rstrip()
                        if content:
                            lines.append(content)
                            lines.append("")

            # ------- INTRODUCCIÓN -------
            intro_folder = None
            for e in os.scandir(subunit_path):
                if e.is_dir() and e.name.lower().startswith("introduction"):
                    intro_folder = Path(e.path)
                    break

            if intro_folder and intro_folder.exists():
                md_files = [
                    Path(f.path) for f in os.scandir(intro_folder)
                    if f.is_file() and f.name.lower().endswith((".md", ".markdown"))
                ]
                md_files.sort(key=lambda p: p.name.lower())
                for md_file in md_files:
                    with md_file.open("r", encoding="utf-8") as f:
                        content = f.read().rstrip()
                        if content:
                            lines.append(content)
                            lines.append("")

            # ------- EJERCICIOS -------
            ejercicios_folder = None
            for e in os.scandir(subunit_path):
                if e.is_dir() and e.name.lower().startswith("101-ejercicios"):
                    ejercicios_folder = Path(e.path)
                    break

            if ejercicios_folder and ejercicios_folder.exists():
                code_files = [
                    Path(f.path) for f in os.scandir(ejercicios_folder)
                    if f.is_file()
                ]
                code_files.sort(key=lambda p: p.name.lower())

                for code_file in code_files:
                    # SALTAR BINARIOS
                    if not is_text_file(code_file):
                        continue

                    exercise_title = title_from_name(code_file.stem)
                    lines.append(f"### {exercise_title}")
                    lines.append("")

                    with code_file.open("r", encoding="utf-8", errors="replace") as f:
                        code = f.read().rstrip("\n")

                    lang = language_from_extension(code_file)
                    lines.append(f"```{lang}".rstrip())
                    lines.append(code)
                    lines.append("```")
                    lines.append("")

        lines.append("")

    with output_path.open("w", encoding="utf-8") as out:
        out.write("\n".join(lines).rstrip() + "\n")

    print(f"Archivo generado: {output_path}")


if __name__ == "__main__":
    import sys
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
    if not root.is_dir():
        print(f"La ruta {root} no es válida.")
        raise SystemExit(1)
    main(root)

