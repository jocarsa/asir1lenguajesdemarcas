import sqlite3
import json

# Conexión a la base de datos SQLite
conn = sqlite3.connect("empresa.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Leer toda la tabla
cursor.execute("SELECT * FROM clientes")
rows = cursor.fetchall()

# Convertir a lista de diccionarios
data = [dict(row) for row in rows]

# Guardar en JSON
with open("clientes.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

conn.close()
