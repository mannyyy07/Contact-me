from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory
import sqlite3
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "doc", "docx", "zip"}

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def connect_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            file_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            reply_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        file_path = None
        token = str(uuid.uuid4())

        # Handle file upload
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
            (name, email, message, token, file_path)
        )
        conn.commit()
        conn.close()

        return redirect(f"/message/{token}")

    return render_template("index.html")

@app.route("/message/<token>")
def view_message(token):
    """Allow users to view their submitted message and replies without login"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message, file_path, created_at FROM messages WHERE token = ?", (token,))
    msg = cursor.fetchone()
    
    if not msg:
        return render_template("404.html"), 404
    
    # Get replies
    cursor.execute("SELECT reply_text, created_at FROM replies WHERE message_id = ? ORDER BY created_at ASC", (msg[0],))
    replies = cursor.fetchall()
    conn.close()
    
    message_data = {
        'id': msg[0],
        'name': msg[1],
        'email': msg[2],
        'message': msg[3],
        'file_path': msg[4],
        'created_at': msg[5],
        'token': token,
        'replies': replies
    }
    
    return render_template("view_message.html", message=message_data)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/messages")
    return render_template("login.html")

@app.route("/messages")
def messages():
    if not session.get("admin"):
        return redirect("/login")

    conn = connect_db()
    cursor = conn.cursor()
    
    # Get search and filter parameters
    search_query = request.args.get("search", "").strip()
    filter_type = request.args.get("filter", "all")  # all, replied, unreplied
    
    # Build query
    query = "SELECT * FROM messages"
    params = []
    
    if search_query:
        query += " WHERE (name LIKE ? OR email LIKE ? OR message LIKE ?)"
        search_param = f"%{search_query}%"
        params = [search_param, search_param, search_param]
    
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    messages_data = cursor.fetchall()
    
    # Get replies for each message and apply filter
    messages_with_replies = []
    unreplied_count = 0
    
    for msg in messages_data:
        cursor.execute("SELECT reply_text, created_at FROM replies WHERE message_id = ? ORDER BY created_at ASC", (msg[0],))
        replies = cursor.fetchall()
        
        msg_dict = {
            'id': msg[0],
            'name': msg[1],
            'email': msg[2],
            'message': msg[3],
            'token': msg[4],
            'file_path': msg[5],
            'created_at': msg[6] if len(msg) > 6 else None,
            'replies': replies,
            'has_replies': len(replies) > 0
        }
        
        # Apply filter
        if filter_type == "replied" and not msg_dict['has_replies']:
            continue
        if filter_type == "unreplied" and msg_dict['has_replies']:
            continue
        
        if not msg_dict['has_replies']:
            unreplied_count += 1
        
        messages_with_replies.append(msg_dict)
    
    conn.close()
    return render_template("messages.html", messages=messages_with_replies, unreplied_count=unreplied_count, 
                         search_query=search_query, filter_type=filter_type)

@app.route("/reply/<int:message_id>", methods=["POST"])
def reply(message_id):
    if not session.get("admin"):
        return redirect("/login")
    
    reply_text = request.form.get("reply_text", "").strip()
    
    if not reply_text:
        return redirect("/messages")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if message exists
    cursor.execute("SELECT email FROM messages WHERE id = ?", (message_id,))
    result = cursor.fetchone()
    
    if result:
        cursor.execute(
            "INSERT INTO replies (message_id, reply_text) VALUES (?, ?)",
            (message_id, reply_text)
        )
        conn.commit()
    
    conn.close()
    return redirect("/messages")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

@app.route("/api/analytics")
def analytics_api():
    """JSON endpoint for analytics data"""
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Total messages
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    
    # Messages with replies
    cursor.execute("""
        SELECT COUNT(DISTINCT message_id) FROM replies
    """)
    replied_messages = cursor.fetchone()[0]
    
    # Unreplied messages
    unreplied = total_messages - replied_messages
    
    # Messages by date (last 7 days)
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM messages
        WHERE created_at >= datetime('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """)
    messages_by_date = cursor.fetchall()
    
    # Average response time (in hours)
    cursor.execute("""
        SELECT AVG((julianday(r.created_at) - julianday(m.created_at)) * 24)
        FROM messages m
        LEFT JOIN replies r ON m.id = r.message_id
        WHERE r.created_at IS NOT NULL
    """)
    avg_response = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_messages': total_messages,
        'replied_messages': replied_messages,
        'unreplied_messages': unreplied,
        'avg_response_hours': round(avg_response, 2) if avg_response else 0,
        'messages_by_date': [{'date': row[0], 'count': row[1]} for row in messages_by_date]
    })

@app.route("/api/set-theme", methods=["POST"])
def set_theme():
    """Store user theme preference"""
    data = request.get_json()
    session['theme'] = data.get('theme', 'light')
    return jsonify({'success': True})

@app.route("/uploads/<filename>")
def download_file(filename):
    """Allow download of attached files"""
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)
    except FileNotFoundError:
        return render_template("404.html"), 404

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
