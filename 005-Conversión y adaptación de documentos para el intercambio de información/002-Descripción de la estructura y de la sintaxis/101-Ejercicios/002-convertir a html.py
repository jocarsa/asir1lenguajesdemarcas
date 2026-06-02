# pip3 install markdown --break-system-packages

import pathlib
import markdown

md_path = pathlib.Path("001-Fundamentos de markdown.md")
html_path = pathlib.Path("003-resultado.html")

text = md_path.read_text(encoding="utf-8")

html_body = markdown.markdown(
    text,
    extensions=[
        "extra",        # tablas, listas mejoradas, etc.
        "toc",          # genera TOC si usas [TOC] o anchors
        "codehilite",   # resalta código (requiere pygments para estilos)
    ],
)

full_html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{md_path.stem}</title>
</head>
<body>
{html_body}
</body>
</html>
"""

html_path.write_text(full_html, encoding="utf-8")
print("OK:", html_path)
