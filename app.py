from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory, flash
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = bool(os.environ.get("VERCEL"))

if os.environ.get("VERCEL") and app.secret_key == "fallback-secret":
    raise RuntimeError("SECRET_KEY must be set in Vercel environment variables.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = "/tmp" if os.environ.get("VERCEL") else BASE_DIR
DB_PATH = os.path.join(RUNTIME_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(RUNTIME_DIR, "uploads")
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "doc", "docx", "zip"}

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "m")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "1")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            file_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            reply_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        contact = request.form.get("contact", "").strip()
        message = request.form.get("message", "").strip()

        if len(name) < 2 or len(contact) < 3 or len(message) < 10:
            flash("Please fill all fields with valid details.", "error")
            return redirect("/")

        file_path = None
        token = str(uuid.uuid4())

        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{token}_{file.filename}")
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                file_path = filename

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (name, email, message, token, file_path) VALUES (?, ?, ?, ?, ?)",
            (name, contact, message, token, file_path),
        )
        conn.commit()
        conn.close()

        return redirect(f"/message/{token}")

    return render_template("index.html")


@app.route("/message/<token>")
def view_message(token):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, message, file_path, created_at FROM messages WHERE token = ?",
        (token,),
    )
    msg = cursor.fetchone()

    if not msg:
        conn.close()
        return render_template("404.html"), 404

    cursor.execute(
        "SELECT reply_text, created_at FROM replies WHERE message_id = ? ORDER BY created_at ASC",
        (msg[0],),
    )
    replies = cursor.fetchall()
    conn.close()

    message_data = {
        "id": msg[0],
        "name": msg[1],
        "email": msg[2],
        "message": msg[3],
        "file_path": msg[4],
        "created_at": msg[5],
        "token": token,
        "replies": replies,
    }

    return render_template("view_message.html", message=message_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USERNAME and request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/messages")

        flash("Invalid admin credentials.", "error")

    return render_template("login.html")


@app.route("/messages")
def messages():
    if not session.get("admin"):
        return redirect("/login")

    conn = connect_db()
    cursor = conn.cursor()

    search_query = request.args.get("search", "").strip()
    filter_type = request.args.get("filter", "all")

    query = "SELECT id, name, email, message, token, file_path, created_at FROM messages"
    params = []

    if search_query:
        query += " WHERE (name LIKE ? OR email LIKE ? OR message LIKE ?)"
        search_param = f"%{search_query}%"
        params = [search_param, search_param, search_param]

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    messages_data = cursor.fetchall()

    messages_with_replies = []
    unreplied_count = 0

    for msg in messages_data:
        cursor.execute("SELECT reply_text, created_at FROM replies WHERE message_id = ? ORDER BY created_at ASC", (msg[0],))
        replies = cursor.fetchall()

        msg_dict = {
            "id": msg[0],
            "name": msg[1],
            "email": msg[2],
            "message": msg[3],
            "token": msg[4],
            "file_path": msg[5],
            "created_at": msg[6],
            "replies": replies,
            "has_replies": len(replies) > 0,
        }

        if filter_type == "replied" and not msg_dict["has_replies"]:
            continue
        if filter_type == "unreplied" and msg_dict["has_replies"]:
            continue

        if not msg_dict["has_replies"]:
            unreplied_count += 1

        messages_with_replies.append(msg_dict)

    conn.close()
    return render_template(
        "messages.html",
        messages=messages_with_replies,
        unreplied_count=unreplied_count,
        search_query=search_query,
        filter_type=filter_type,
    )


@app.route("/reply/<int:message_id>", methods=["POST"])
def reply(message_id):
    if not session.get("admin"):
        return redirect("/login")

    reply_text = request.form.get("reply_text", "").strip()
    if not reply_text:
        return redirect("/messages")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM messages WHERE id = ?", (message_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("INSERT INTO replies (message_id, reply_text) VALUES (?, ?)", (message_id, reply_text))
        conn.commit()

    conn.close()
    return redirect("/messages")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


@app.route("/api/analytics")
def analytics_api():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT message_id) FROM replies")
    replied_messages = cursor.fetchone()[0]

    unreplied = total_messages - replied_messages

    cursor.execute(
        """
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM messages
        WHERE created_at >= datetime('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
        """
    )
    messages_by_date = cursor.fetchall()

    cursor.execute(
        """
        SELECT AVG((julianday(r.created_at) - julianday(m.created_at)) * 24)
        FROM messages m
        LEFT JOIN replies r ON m.id = r.message_id
        WHERE r.created_at IS NOT NULL
        """
    )
    avg_response = cursor.fetchone()[0]

    conn.close()

    return jsonify(
        {
            "total_messages": total_messages,
            "replied_messages": replied_messages,
            "unreplied_messages": unreplied,
            "avg_response_hours": round(avg_response, 2) if avg_response else 0,
            "messages_by_date": [{"date": row[0], "count": row[1]} for row in messages_by_date],
        }
    )


@app.route("/api/set-theme", methods=["POST"])
def set_theme():
    data = request.get_json()
    session["theme"] = data.get("theme", "dark")
    return jsonify({"success": True})


@app.route("/uploads/<filename>")
def download_file(filename):
    token = request.args.get("token", "")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT token FROM messages WHERE file_path = ?", (filename,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return render_template("404.html"), 404

    if not session.get("admin") and (not token or token != row[0]):
        return render_template("404.html"), 404

    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)
    except FileNotFoundError:
        return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
