import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash


APP_NAME = "jocarsa | microsaas"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET", "dev-secret-change-me")

    # DB en carpeta instance/
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["DATABASE"] = os.path.join(app.instance_path, "microsaas.db")

    def get_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db():
        conn = get_db()
        cur = conn.cursor()

        # Users (login)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)

        # Clientes
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            direccion TEXT,
            created_at TEXT NOT NULL
        );
        """)

        # Productos
        cur.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            sku TEXT,
            precio REAL NOT NULL DEFAULT 0,
            stock INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );
        """)

        # Pedidos (cabecera)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pedidos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'borrador',
            notas TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
        );
        """)

        # Líneas de pedido
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pedido_lineas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            precio_unitario REAL NOT NULL DEFAULT 0,
            FOREIGN KEY(pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
            FOREIGN KEY(producto_id) REFERENCES productos(id) ON DELETE RESTRICT
        );
        """)

        # Seed: usuario por defecto
        cur.execute("SELECT id FROM users WHERE username = ?", ("jocarsa",))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO users(username, password_hash, created_at) VALUES(?,?,?)",
                ("jocarsa", generate_password_hash("jocarsa"), datetime.utcnow().isoformat())
            )

        conn.commit()
        conn.close()

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped

    @app.context_processor
    def inject_globals():
        return {
            "APP_NAME": APP_NAME,
            "current_user": session.get("username")
        }

    @app.route("/")
    def home():
        if session.get("user_id"):
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

            conn = get_db()
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            conn.close()

            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("dashboard"))

            flash("Credenciales incorrectas.", "error")
            return redirect(url_for("login"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    # -------------------------
    # CLIENTES CRUD
    # -------------------------
    @app.route("/clientes")
    @login_required
    def clientes_list():
        q = (request.args.get("q") or "").strip()
        conn = get_db()
        if q:
            rows = conn.execute("""
                SELECT * FROM clientes
                WHERE nombre LIKE ? OR apellidos LIKE ? OR email LIKE ?
                ORDER BY id DESC
            """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
        else:
            rows = conn.execute("SELECT * FROM clientes ORDER BY id DESC").fetchall()
        conn.close()
        return render_template("clientes_list.html", clientes=rows, q=q)

    @app.route("/clientes/nuevo", methods=["GET", "POST"])
    @login_required
    def clientes_new():
        if request.method == "POST":
            data = {
                "nombre": (request.form.get("nombre") or "").strip(),
                "apellidos": (request.form.get("apellidos") or "").strip(),
                "email": (request.form.get("email") or "").strip(),
                "telefono": (request.form.get("telefono") or "").strip(),
                "direccion": (request.form.get("direccion") or "").strip(),
            }
            if not data["nombre"] or not data["apellidos"]:
                flash("Nombre y apellidos son obligatorios.", "error")
                return redirect(url_for("clientes_new"))

            conn = get_db()
            conn.execute("""
                INSERT INTO clientes(nombre, apellidos, email, telefono, direccion, created_at)
                VALUES(?,?,?,?,?,?)
            """, (
                data["nombre"], data["apellidos"], data["email"], data["telefono"], data["direccion"],
                datetime.utcnow().isoformat()
            ))
            conn.commit()
            conn.close()
            flash("Cliente creado.", "ok")
            return redirect(url_for("clientes_list"))

        return render_template("clientes_form.html", mode="new", cliente=None)

    @app.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
    @login_required
    def clientes_edit(cliente_id):
        conn = get_db()
        cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
        if not cliente:
            conn.close()
            flash("Cliente no encontrado.", "error")
            return redirect(url_for("clientes_list"))

        if request.method == "POST":
            data = {
                "nombre": (request.form.get("nombre") or "").strip(),
                "apellidos": (request.form.get("apellidos") or "").strip(),
                "email": (request.form.get("email") or "").strip(),
                "telefono": (request.form.get("telefono") or "").strip(),
                "direccion": (request.form.get("direccion") or "").strip(),
            }
            if not data["nombre"] or not data["apellidos"]:
                conn.close()
                flash("Nombre y apellidos son obligatorios.", "error")
                return redirect(url_for("clientes_edit", cliente_id=cliente_id))

            conn.execute("""
                UPDATE clientes
                SET nombre=?, apellidos=?, email=?, telefono=?, direccion=?
                WHERE id=?
            """, (
                data["nombre"], data["apellidos"], data["email"], data["telefono"], data["direccion"],
                cliente_id
            ))
            conn.commit()
            conn.close()
            flash("Cliente actualizado.", "ok")
            return redirect(url_for("clientes_list"))

        conn.close()
        return render_template("clientes_form.html", mode="edit", cliente=cliente)

    @app.route("/clientes/<int:cliente_id>/borrar", methods=["POST"])
    @login_required
    def clientes_delete(cliente_id):
        conn = get_db()
        try:
            conn.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            conn.commit()
            flash("Cliente borrado.", "ok")
        except sqlite3.IntegrityError:
            flash("No se puede borrar: el cliente tiene pedidos asociados.", "error")
        finally:
            conn.close()
        return redirect(url_for("clientes_list"))

    # -------------------------
    # PRODUCTOS CRUD
    # -------------------------
    @app.route("/productos")
    @login_required
    def productos_list():
        q = (request.args.get("q") or "").strip()
        conn = get_db()
        if q:
            rows = conn.execute("""
                SELECT * FROM productos
                WHERE nombre LIKE ? OR sku LIKE ?
                ORDER BY id DESC
            """, (f"%{q}%", f"%{q}%")).fetchall()
        else:
            rows = conn.execute("SELECT * FROM productos ORDER BY id DESC").fetchall()
        conn.close()
        return render_template("productos_list.html", productos=rows, q=q)

    @app.route("/productos/nuevo", methods=["GET", "POST"])
    @login_required
    def productos_new():
        if request.method == "POST":
            nombre = (request.form.get("nombre") or "").strip()
            sku = (request.form.get("sku") or "").strip()
            precio = request.form.get("precio") or "0"
            stock = request.form.get("stock") or "0"

            if not nombre:
                flash("El nombre es obligatorio.", "error")
                return redirect(url_for("productos_new"))

            try:
                precio_f = float(precio)
            except ValueError:
                precio_f = 0.0
            try:
                stock_i = int(stock)
            except ValueError:
                stock_i = 0

            conn = get_db()
            conn.execute("""
                INSERT INTO productos(nombre, sku, precio, stock, created_at)
                VALUES(?,?,?,?,?)
            """, (nombre, sku, precio_f, stock_i, datetime.utcnow().isoformat()))
            conn.commit()
            conn.close()
            flash("Producto creado.", "ok")
            return redirect(url_for("productos_list"))

        return render_template("productos_form.html", mode="new", producto=None)

    @app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
    @login_required
    def productos_edit(producto_id):
        conn = get_db()
        producto = conn.execute("SELECT * FROM productos WHERE id = ?", (producto_id,)).fetchone()
        if not producto:
            conn.close()
            flash("Producto no encontrado.", "error")
            return redirect(url_for("productos_list"))

        if request.method == "POST":
            nombre = (request.form.get("nombre") or "").strip()
            sku = (request.form.get("sku") or "").strip()
            precio = request.form.get("precio") or "0"
            stock = request.form.get("stock") or "0"

            if not nombre:
                conn.close()
                flash("El nombre es obligatorio.", "error")
                return redirect(url_for("productos_edit", producto_id=producto_id))

            try:
                precio_f = float(precio)
            except ValueError:
                precio_f = 0.0
            try:
                stock_i = int(stock)
            except ValueError:
                stock_i = 0

            conn.execute("""
                UPDATE productos
                SET nombre=?, sku=?, precio=?, stock=?
                WHERE id=?
            """, (nombre, sku, precio_f, stock_i, producto_id))
            conn.commit()
            conn.close()
            flash("Producto actualizado.", "ok")
            return redirect(url_for("productos_list"))

        conn.close()
        return render_template("productos_form.html", mode="edit", producto=producto)

    @app.route("/productos/<int:producto_id>/borrar", methods=["POST"])
    @login_required
    def productos_delete(producto_id):
        conn = get_db()
        try:
            conn.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            conn.commit()
            flash("Producto borrado.", "ok")
        except sqlite3.IntegrityError:
            flash("No se puede borrar: el producto está en líneas de pedido.", "error")
        finally:
            conn.close()
        return redirect(url_for("productos_list"))

    # -------------------------
    # PEDIDOS
    # -------------------------
    @app.route("/pedidos")
    @login_required
    def pedidos_list():
        conn = get_db()
        rows = conn.execute("""
            SELECT p.*, c.nombre || ' ' || c.apellidos AS cliente_nombre
            FROM pedidos p
            JOIN clientes c ON c.id = p.cliente_id
            ORDER BY p.id DESC
        """).fetchall()
        conn.close()
        return render_template("pedidos_list.html", pedidos=rows)

    @app.route("/pedidos/nuevo", methods=["GET", "POST"])
    @login_required
    def pedidos_new():
        conn = get_db()
        clientes = conn.execute("SELECT id, nombre, apellidos FROM clientes ORDER BY apellidos, nombre").fetchall()
        productos = conn.execute("SELECT id, nombre, precio FROM productos ORDER BY nombre").fetchall()

        if request.method == "POST":
            cliente_id = request.form.get("cliente_id") or ""
            estado = (request.form.get("estado") or "borrador").strip()
            notas = (request.form.get("notas") or "").strip()

            # Líneas (3 filas fijas sin JS)
            lineas = []
            for i in range(1, 4):
                pid = request.form.get(f"producto_{i}") or ""
                cant = request.form.get(f"cantidad_{i}") or ""
                precio = request.form.get(f"precio_{i}") or ""

                if not pid:
                    continue
                try:
                    cant_i = int(cant) if cant else 1
                except ValueError:
                    cant_i = 1
                try:
                    precio_f = float(precio) if precio else 0.0
                except ValueError:
                    precio_f = 0.0

                lineas.append((int(pid), max(1, cant_i), max(0.0, precio_f)))

            if not cliente_id:
                conn.close()
                flash("Selecciona un cliente.", "error")
                return redirect(url_for("pedidos_new"))

            if len(lineas) == 0:
                conn.close()
                flash("Añade al menos una línea de pedido.", "error")
                return redirect(url_for("pedidos_new"))

            now = datetime.utcnow().isoformat()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pedidos(cliente_id, fecha, estado, notas, created_at)
                VALUES(?,?,?,?,?)
            """, (int(cliente_id), datetime.utcnow().date().isoformat(), estado, notas, now))
            pedido_id = cur.lastrowid

            for (producto_id, cantidad, precio_unitario) in lineas:
                cur.execute("""
                    INSERT INTO pedido_lineas(pedido_id, producto_id, cantidad, precio_unitario)
                    VALUES(?,?,?,?)
                """, (pedido_id, producto_id, cantidad, precio_unitario))

            conn.commit()
            conn.close()
            flash("Pedido creado.", "ok")
            return redirect(url_for("pedido_view", pedido_id=pedido_id))

        conn.close()
        return render_template("pedidos_form.html", clientes=clientes, productos=productos)

    @app.route("/pedidos/<int:pedido_id>")
    @login_required
    def pedido_view(pedido_id):
        conn = get_db()
        pedido = conn.execute("""
            SELECT p.*, c.nombre || ' ' || c.apellidos AS cliente_nombre
            FROM pedidos p
            JOIN clientes c ON c.id = p.cliente_id
            WHERE p.id = ?
        """, (pedido_id,)).fetchone()

        if not pedido:
            conn.close()
            flash("Pedido no encontrado.", "error")
            return redirect(url_for("pedidos_list"))

        lineas = conn.execute("""
            SELECT l.*, pr.nombre AS producto_nombre
            FROM pedido_lineas l
            JOIN productos pr ON pr.id = l.producto_id
            WHERE l.pedido_id = ?
            ORDER BY l.id ASC
        """, (pedido_id,)).fetchall()

        total = 0.0
        for l in lineas:
            total += float(l["cantidad"]) * float(l["precio_unitario"])

        conn.close()
        return render_template("pedido_view.html", pedido=pedido, lineas=lineas, total=total)

    @app.route("/pedidos/<int:pedido_id>/borrar", methods=["POST"])
    @login_required
    def pedido_delete(pedido_id):
        conn = get_db()
        conn.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
        conn.commit()
        conn.close()
        flash("Pedido borrado.", "ok")
        return redirect(url_for("pedidos_list"))

    # Inicializa DB al arrancar
    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)