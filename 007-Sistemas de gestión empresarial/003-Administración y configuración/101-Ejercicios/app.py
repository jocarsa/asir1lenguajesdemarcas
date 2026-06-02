from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "CAMBIA_ESTA_CLAVE_SECRETA"

DB_CONFIG = {
    "host": "localhost",
    "user": "ticketing",
    "password": "ticketing",
    "database": "ticketing",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "txt", "log", "zip"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def db():
    return mysql.connector.connect(**DB_CONFIG)


def query_all(sql, params=None):
    conn = db()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def query_one(sql, params=None):
    rows = query_all(sql, params)
    return rows[0] if rows else None


def execute(sql, params=None):
    conn = db()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    last_id = cur.lastrowid
    cur.close()
    conn.close()
    return last_id


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def require_admin():
    if not session.get("admin_user_id"):
        return redirect(url_for("admin_login"))
    return None


@app.context_processor
def inject_now():
    return {"now": datetime.now()}


# =========================
# BLOQUE PÚBLICO
# =========================

@app.get("/")
def public_new_ticket():
    categories = query_all("SELECT id, name FROM categories WHERE is_active=1 ORDER BY name")
    return render_template("public_new_ticket.html", categories=categories)


@app.post("/ticket")
def public_create_ticket():
    requester_name = (request.form.get("requester_name") or "").strip()
    title = (request.form.get("title") or "").strip()
    description = (request.form.get("description") or "").strip()
    category_id = request.form.get("category_id")

    if not requester_name or not title or not description or not category_id:
        flash("Faltan campos obligatorios.", "error")
        return redirect(url_for("public_new_ticket"))

    default_status = query_one("SELECT id FROM statuses WHERE name='Nuevo' LIMIT 1")
    if not default_status:
        # fallback: primer estado activo
        default_status = query_one("SELECT id FROM statuses WHERE is_active=1 ORDER BY id LIMIT 1")
    if not default_status:
        flash("No hay estados configurados. Contacta con el administrador.", "error")
        return redirect(url_for("public_new_ticket"))

    attachment_original = None
    attachment_stored = None

    f = request.files.get("attachment")
    if f and f.filename:
        if not allowed_file(f.filename):
            flash("Tipo de archivo no permitido.", "error")
            return redirect(url_for("public_new_ticket"))

        attachment_original = f.filename
        safe = secure_filename(f.filename)
        stored = f"{uuid.uuid4().hex}_{safe}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], stored)
        f.save(save_path)
        attachment_stored = stored

    ticket_id = execute(
        """
        INSERT INTO tickets
          (requester_name, title, description, category_id, status_id,
           attachment_original_name, attachment_stored_name, created_at)
        VALUES
          (%s, %s, %s, %s, %s, %s, %s, NOW())
        """,
        (requester_name, title, description, int(category_id), int(default_status["id"]),
         attachment_original, attachment_stored)
    )

    return render_template("public_ticket_ok.html", ticket_id=ticket_id)


# =========================
# AUTH ADMIN
# =========================

@app.get("/admin/login")
def admin_login():
    return render_template("admin_login.html")


@app.post("/admin/login")
def admin_login_post():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    user = query_one("SELECT id, username, password_hash FROM admin_users WHERE username=%s LIMIT 1", (username,))
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Credenciales incorrectas.", "error")
        return redirect(url_for("admin_login"))

    session["admin_user_id"] = user["id"]
    session["admin_username"] = user["username"]
    return redirect(url_for("admin_dashboard"))


@app.get("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# Endpoint auxiliar para crear hash correcto de demo (una sola vez)
@app.get("/admin/init-demo")
def admin_init_demo():
    """
    Crea/actualiza usuario admin=admin con password=admin123
    Úsalo una vez y luego elimina este endpoint si lo deseas.
    """
    username = "admin"
    pwd = "admin123"
    ph = generate_password_hash(pwd)

    existing = query_one("SELECT id FROM admin_users WHERE username=%s", (username,))
    if existing:
        execute("UPDATE admin_users SET password_hash=%s WHERE id=%s", (ph, existing["id"]))
    else:
        execute("INSERT INTO admin_users (username, password_hash) VALUES (%s, %s)", (username, ph))

    return (
        "OK. Usuario demo listo: admin / admin123. "
        "Ahora puedes borrar el endpoint /admin/init-demo por seguridad."
    )


# =========================
# PANEL ADMIN
# =========================

@app.get("/admin")
def admin_dashboard():
    r = require_admin()
    if r:
        return r

    counts = {
        "tickets_total": query_one("SELECT COUNT(*) AS c FROM tickets")["c"],
        "tickets_new": query_one(
            "SELECT COUNT(*) AS c FROM tickets t JOIN statuses s ON s.id=t.status_id WHERE s.name='Nuevo'"
        )["c"],
        "categories": query_one("SELECT COUNT(*) AS c FROM categories")["c"],
        "statuses": query_one("SELECT COUNT(*) AS c FROM statuses")["c"],
    }
    return render_template("admin_dashboard.html", counts=counts)


# ----- CATEGORIES CRUD -----

@app.get("/admin/categories")
def admin_categories_list():
    r = require_admin()
    if r:
        return r
    rows = query_all("SELECT * FROM categories ORDER BY name")
    return render_template("admin_categories_list.html", rows=rows)


@app.get("/admin/categories/new")
def admin_categories_new():
    r = require_admin()
    if r:
        return r
    return render_template("admin_categories_form.html", row=None)


@app.post("/admin/categories/new")
def admin_categories_create():
    r = require_admin()
    if r:
        return r
    name = (request.form.get("name") or "").strip()
    is_active = 1 if request.form.get("is_active") == "1" else 0
    if not name:
        flash("El nombre es obligatorio.", "error")
        return redirect(url_for("admin_categories_new"))
    execute("INSERT INTO categories (name, is_active) VALUES (%s, %s)", (name, is_active))
    flash("Categoría creada.", "ok")
    return redirect(url_for("admin_categories_list"))


@app.get("/admin/categories/edit/<int:id>")
def admin_categories_edit(id):
    r = require_admin()
    if r:
        return r
    row = query_one("SELECT * FROM categories WHERE id=%s", (id,))
    if not row:
        abort(404)
    return render_template("admin_categories_form.html", row=row)


@app.post("/admin/categories/edit/<int:id>")
def admin_categories_update(id):
    r = require_admin()
    if r:
        return r
    name = (request.form.get("name") or "").strip()
    is_active = 1 if request.form.get("is_active") == "1" else 0
    if not name:
        flash("El nombre es obligatorio.", "error")
        return redirect(url_for("admin_categories_edit", id=id))
    execute("UPDATE categories SET name=%s, is_active=%s WHERE id=%s", (name, is_active, id))
    flash("Categoría actualizada.", "ok")
    return redirect(url_for("admin_categories_list"))


@app.post("/admin/categories/delete/<int:id>")
def admin_categories_delete(id):
    r = require_admin()
    if r:
        return r
    try:
        execute("DELETE FROM categories WHERE id=%s", (id,))
        flash("Categoría eliminada.", "ok")
    except mysql.connector.Error:
        flash("No se puede eliminar: está en uso por tickets.", "error")
    return redirect(url_for("admin_categories_list"))


# ----- STATUSES CRUD -----

@app.get("/admin/statuses")
def admin_statuses_list():
    r = require_admin()
    if r:
        return r
    rows = query_all("SELECT * FROM statuses ORDER BY id")
    return render_template("admin_statuses_list.html", rows=rows)


@app.get("/admin/statuses/new")
def admin_statuses_new():
    r = require_admin()
    if r:
        return r
    return render_template("admin_statuses_form.html", row=None)


@app.post("/admin/statuses/new")
def admin_statuses_create():
    r = require_admin()
    if r:
        return r
    name = (request.form.get("name") or "").strip()
    is_active = 1 if request.form.get("is_active") == "1" else 0
    if not name:
        flash("El nombre es obligatorio.", "error")
        return redirect(url_for("admin_statuses_new"))
    execute("INSERT INTO statuses (name, is_active) VALUES (%s, %s)", (name, is_active))
    flash("Estado creado.", "ok")
    return redirect(url_for("admin_statuses_list"))


@app.get("/admin/statuses/edit/<int:id>")
def admin_statuses_edit(id):
    r = require_admin()
    if r:
        return r
    row = query_one("SELECT * FROM statuses WHERE id=%s", (id,))
    if not row:
        abort(404)
    return render_template("admin_statuses_form.html", row=row)


@app.post("/admin/statuses/edit/<int:id>")
def admin_statuses_update(id):
    r = require_admin()
    if r:
        return r
    name = (request.form.get("name") or "").strip()
    is_active = 1 if request.form.get("is_active") == "1" else 0
    if not name:
        flash("El nombre es obligatorio.", "error")
        return redirect(url_for("admin_statuses_edit", id=id))
    execute("UPDATE statuses SET name=%s, is_active=%s WHERE id=%s", (name, is_active, id))
    flash("Estado actualizado.", "ok")
    return redirect(url_for("admin_statuses_list"))


@app.post("/admin/statuses/delete/<int:id>")
def admin_statuses_delete(id):
    r = require_admin()
    if r:
        return r
    try:
        execute("DELETE FROM statuses WHERE id=%s", (id,))
        flash("Estado eliminado.", "ok")
    except mysql.connector.Error:
        flash("No se puede eliminar: está en uso por tickets.", "error")
    return redirect(url_for("admin_statuses_list"))


# ----- TICKETS CRUD + FILTROS -----

@app.get("/admin/tickets")
def admin_tickets_list():
    r = require_admin()
    if r:
        return r

    f_status = (request.args.get("status_id") or "").strip()
    f_category = (request.args.get("category_id") or "").strip()
    q = (request.args.get("q") or "").strip()

    where = []
    params = []

    if f_status.isdigit():
        where.append("t.status_id = %s")
        params.append(int(f_status))

    if f_category.isdigit():
        where.append("t.category_id = %s")
        params.append(int(f_category))

    if q:
        like = f"%{q}%"
        where.append("(t.requester_name LIKE %s OR t.title LIKE %s OR t.description LIKE %s)")
        params.extend([like, like, like])

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    # IDs de estados "finales"
    st_resuelto = query_one("SELECT id FROM statuses WHERE name='Resuelto' LIMIT 1")
    st_cerrado  = query_one("SELECT id FROM statuses WHERE name='Cerrado' LIMIT 1")

    resuelto_id = st_resuelto["id"] if st_resuelto else None
    cerrado_id  = st_cerrado["id"] if st_cerrado else None

    finales = [x for x in [resuelto_id, cerrado_id] if x is not None]

    # Si por lo que sea no existen, no segregamos (pero normalmente existen)
    if not finales:
        base_sql = f"""
            SELECT t.*, c.name AS category_name, s.name AS status_name
            FROM tickets t
            JOIN categories c ON c.id=t.category_id
            JOIN statuses s ON s.id=t.status_id
            {where_sql}
            ORDER BY t.created_at DESC
        """
        all_rows = query_all(base_sql, tuple(params))
        open_rows = all_rows
        closed_rows = []
    else:
        # Abiertos: NOT IN (resuelto, cerrado)
        open_sql = f"""
            SELECT t.*, c.name AS category_name, s.name AS status_name
            FROM tickets t
            JOIN categories c ON c.id=t.category_id
            JOIN statuses s ON s.id=t.status_id
            {where_sql}
            {"AND" if where_sql else "WHERE"} t.status_id NOT IN ({",".join(["%s"]*len(finales))})
            ORDER BY t.created_at DESC
        """

        # Cerrados: IN (resuelto, cerrado)
        closed_sql = f"""
            SELECT t.*, c.name AS category_name, s.name AS status_name
            FROM tickets t
            JOIN categories c ON c.id=t.category_id
            JOIN statuses s ON s.id=t.status_id
            {where_sql}
            {"AND" if where_sql else "WHERE"} t.status_id IN ({",".join(["%s"]*len(finales))})
            ORDER BY t.created_at DESC
        """

        open_rows = query_all(open_sql, tuple(params + finales))
        closed_rows = query_all(closed_sql, tuple(params + finales))

    categories = query_all("SELECT id, name FROM categories ORDER BY name")
    statuses = query_all("SELECT id, name FROM statuses ORDER BY id")

    return render_template(
        "admin_tickets_list.html",
        open_rows=open_rows,
        closed_rows=closed_rows,
        categories=categories,
        statuses=statuses,
        f_status=f_status,
        f_category=f_category,
        q=q
    )


@app.get("/admin/tickets/view/<int:id>")
def admin_tickets_view(id):
    r = require_admin()
    if r:
        return r

    row = query_one(
        """
        SELECT
          t.*,
          c.name AS category_name,
          s.name AS status_name
        FROM tickets t
        JOIN categories c ON c.id=t.category_id
        JOIN statuses s ON s.id=t.status_id
        WHERE t.id=%s
        """,
        (id,)
    )
    if not row:
        abort(404)

    return render_template("admin_tickets_view.html", row=row)


@app.get("/admin/tickets/edit/<int:id>")
def admin_tickets_edit(id):
    r = require_admin()
    if r:
        return r

    row = query_one("SELECT * FROM tickets WHERE id=%s", (id,))
    if not row:
        abort(404)

    categories = query_all("SELECT id, name FROM categories WHERE is_active=1 ORDER BY name")
    statuses = query_all("SELECT id, name FROM statuses WHERE is_active=1 ORDER BY id")

    return render_template("admin_tickets_edit.html", row=row, categories=categories, statuses=statuses)


@app.post("/admin/tickets/edit/<int:id>")
def admin_tickets_update(id):
    r = require_admin()
    if r:
        return r

    category_id = request.form.get("category_id") or ""
    status_id = request.form.get("status_id") or ""

    if not category_id.isdigit() or not status_id.isdigit():
        flash("Categoría/Estado inválidos.", "error")
        return redirect(url_for("admin_tickets_edit", id=id))

    execute(
        """
        UPDATE tickets
        SET category_id=%s, status_id=%s, updated_at=NOW()
        WHERE id=%s
        """,
        (int(category_id), int(status_id), id)
    )

    flash("Ticket actualizado.", "ok")
    return redirect(url_for("admin_tickets_view", id=id))


@app.post("/admin/tickets/delete/<int:id>")
def admin_tickets_delete(id):
    r = require_admin()
    if r:
        return r

    row = query_one("SELECT attachment_stored_name FROM tickets WHERE id=%s", (id,))
    if not row:
        abort(404)

    # borrado archivo adjunto si existe
    stored = row.get("attachment_stored_name")
    if stored:
        path = os.path.join(app.config["UPLOAD_FOLDER"], stored)
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass

    execute("DELETE FROM tickets WHERE id=%s", (id,))
    flash("Ticket eliminado.", "ok")
    return redirect(url_for("admin_tickets_list"))


@app.get("/uploads/<path:filename>")
def download_upload(filename):
    # Por simplicidad: solo admin puede descargar adjuntos
    if not session.get("admin_user_id"):
        return redirect(url_for("admin_login"))
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
