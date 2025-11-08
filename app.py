from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from collections import deque
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

login_manager = LoginManager(app)
login_manager.login_view = "index"  # redirect here when not logged in

DB_PATH = "users.db"

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
init_db()

class User(UserMixin):
    def __init__(self, id_, username, password_hash):
        self.id = str(id_)
        self.username = username
        self.password_hash = password_hash

def get_user_by_username(username):
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,)).fetchone()
    return User(*row) if row else None

def get_user_by_id(user_id):
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute("SELECT id, username, password_hash FROM users WHERE id = ?", (user_id,)).fetchone()
    return User(*row) if row else None

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# in-memory demo data
MESSAGES = deque(maxlen=200)
FLIGHTS = [
    {"flight":"AA123", "from":"RDU", "to":"CLT", "dep":"2025-11-08T09:15", "arr":"2025-11-08T10:10"},
    {"flight":"DL456", "from":"GSO", "to":"ATL", "dep":"2025-11-08T12:05", "arr":"2025-11-08T13:25"},
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# auth routes
@app.post("/register")
def register():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if not username or not password:
        flash("Username and password required")
        return redirect(url_for("index"))
    if get_user_by_username(username):
        flash("Username already exists")
        return redirect(url_for("index"))
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO users(username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
    user = get_user_by_username(username)
    login_user(user)
    return redirect(url_for("index"))

@app.post("/login")
def login():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    user = get_user_by_username(username)
    if not user or not check_password_hash(user.password_hash, password):
        flash("Invalid credentials")
        return redirect(url_for("index"))
    login_user(user)
    return redirect(url_for("index"))

@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# chat APIs
@app.get("/api/messages")
@login_required
def get_messages():
    since = request.args.get("since")
    if since:
        try:
            cutoff = datetime.fromisoformat(since)
            items = [m for m in MESSAGES if datetime.fromisoformat(m["ts"]) > cutoff]
            return jsonify(items)
        except Exception:
            pass
    return jsonify(list(MESSAGES))

@app.post("/api/messages")
@login_required
def post_message():
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    user = current_user.username or "anon"
    if not text:
        return jsonify({"ok": False, "error": "empty"}), 400
    msg = {"user": user[:32], "text": text[:2000], "ts": datetime.utcnow().isoformat()}
    MESSAGES.append(msg)
    return jsonify({"ok": True})

# flights API
@app.get("/api/flights")
@login_required
def get_flights():
    return jsonify(FLIGHTS)

if __name__ == "__main__":
    app.run(debug=True)
