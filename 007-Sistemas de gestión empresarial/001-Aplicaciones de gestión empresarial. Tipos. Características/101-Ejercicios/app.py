from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "cambia-esto-por-una-clave"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "clientes.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                direccion TEXT
            )
        """)
        conn.commit()

@app.route("/")
def index():
    q = (request.args.get("q") or "").strip()
    with get_conn() as conn:
        if q:
            clientes = conn.execute("""
                SELECT * FROM clientes
                WHERE nombre LIKE ? OR apellidos LIKE ? OR email LIKE ?
                ORDER BY apellidos, nombre
            """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
        else:
            clientes = conn.execute("""
                SELECT * FROM clientes
                ORDER BY apellidos, nombre
            """).fetchall()

    return render_template("index.html", clientes=clientes, q=q)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()
        apellidos = (request.form.get("apellidos") or "").strip()
        email = (request.form.get("email") or "").strip()
        telefono = (request.form.get("telefono") or "").strip()
        direccion = (request.form.get("direccion") or "").strip()

        if not nombre or not apellidos:
            flash("Nombre y apellidos son obligatorios.", "error")
            return render_template("nuevo.html", form=request.form)

        with get_conn() as conn:
            conn.execute("""
                INSERT INTO clientes (nombre, apellidos, email, telefono, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, apellidos, email, telefono, direccion))
            conn.commit()

        flash("Cliente creado correctamente.", "ok")
        return redirect(url_for("index"))

    return render_template("nuevo.html", form={})

@app.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    with get_conn() as conn:
        cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()

    if not cliente:
        flash("Cliente no encontrado.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()
        apellidos = (request.form.get("apellidos") or "").strip()
        email = (request.form.get("email") or "").strip()
        telefono = (request.form.get("telefono") or "").strip()
        direccion = (request.form.get("direccion") or "").strip()

        if not nombre or not apellidos:
            flash("Nombre y apellidos son obligatorios.", "error")
            return render_template("editar.html", cliente=cliente, form=request.form)

        with get_conn() as conn:
            conn.execute("""
                UPDATE clientes
                SET nombre = ?, apellidos = ?, email = ?, telefono = ?, direccion = ?
                WHERE id = ?
            """, (nombre, apellidos, email, telefono, direccion, cliente_id))
            conn.commit()

        flash("Cliente actualizado correctamente.", "ok")
        return redirect(url_for("index"))

    return render_template("editar.html", cliente=cliente, form=dict(cliente))

@app.route("/clientes/<int:cliente_id>/borrar", methods=["POST"])
def borrar(cliente_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conn.commit()
    flash("Cliente eliminado.", "ok")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)