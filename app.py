from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from collections import deque
from datetime import datetime
import sqlite3
import os
from config import API_KEY, BASE_URL
from services.flight_api import get_flights

SERVER_USER = "admin"
SERVER_PASS = "password"

def decrypt_letter_wingding(letterinWord: str) -> str:
    output = ""
    decrypt_map = {
        "U0001F61C": "a","U0001F628": "b","U0001F485": "c","U0001F9AC": "d","U0001F348": "e",
        "U0001F9C2": "f","U00026E9": "g","U0001F31D": "h","U0001F31A": "i","U0001F3B2": "j",
        "U0001F338": "k","U0001F495": "l","U0001F973": "m","U0001F9E9": "n","U0001F393": "o",
        "U0002702": "p","U0001FAE7": "q","U000262E": "r","U000269C": "s","U0001F7E3": "t",
        "U000264F": "u","U000264B": "v","U0001F92F": "w","U000264D": "x","U0001F4B0": "y","U0001F9E6": "z"
    }

    for i in range(0, len(letterinWord), 8):
        code = letterinWord[i:i+8]
        if code in decrypt_map:
            output += decrypt_map[code]
    return output


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

def is_encrypted_text(txt: str) -> bool:
    # PoC rule: treat messages starting with "ENC:" as encrypted
    return txt.strip().startswith("ENC:")


# chat APIs
@app.get("/api/messages")
@login_required
def get_messages():
    since = request.args.get("since")
    encrypted_only = request.args.get("encrypted") in ("1", "true", "True")

    def after_since(items):
        if since:
            try:
                cutoff = datetime.fromisoformat(since)
                return [m for m in items if datetime.fromisoformat(m["ts"]) > cutoff]
            except Exception:
                return items
        return items

    items = list(MESSAGES)
    if encrypted_only:
        items = [m for m in items if is_encrypted_text(m["text"])]
    return jsonify(after_since(items))

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

# --- Server console auth (separate from Flask-Login) ---
@app.get("/server")
def server_console():
    if not session.get("server_auth"):
        return render_template("server_login.html")
    return render_template("server_console.html")

@app.post("/server_login")
def server_login():
    u = (request.form.get("username") or "").strip()
    p = request.form.get("password") or ""
    if u == SERVER_USER and p == SERVER_PASS:
        session["server_auth"] = True
        return redirect(url_for("server_console"))
    flash("Invalid server credentials")
    return redirect(url_for("server_console"))

@app.get("/server_logout")
def server_logout():
    session.pop("server_auth", None)
    return redirect(url_for("server_console"))

# --- API for console: always encrypted-only, no user login required but gated by server_auth ---
@app.get("/api/server/encrypted")
def server_encrypted_feed():
    if not session.get("server_auth"):
        return jsonify({"error": "unauthorized"}), 401
    since = request.args.get("since")
    items = [m for m in MESSAGES if is_encrypted_text(m["text"])]
    if since:
        try:
            cutoff = datetime.fromisoformat(since)
            items = [m for m in items if datetime.fromisoformat(m["ts"]) > cutoff]
        except Exception:
            pass
    return jsonify(items)


@app.route("/api/airports")
@login_required
def api_airports():
    """
    Returns all NC airports (public + private).
    """
    # Example data: Ideally you'd pull from an external API like FAA, OpenSky, or AirLabs
    # or from a prebuilt nc_airports.json file you maintain.
    nc_airports = [
        {"name": "Charlotte Douglas International", "code": "CLT"},
        {"name": "Raleigh–Durham International", "code": "RDU"},
        {"name": "Piedmont Triad International", "code": "GSO"},
        {"name": "Wilmington International", "code": "ILM"},
        {"name": "Asheville Regional", "code": "AVL"},
        {"name": "Fayetteville Regional", "code": "FAY"},
        {"name": "Coastal Carolina Regional", "code": "EWN"},
        {"name": "Albert J. Ellis", "code": "OAJ"},
        {"name": "Concord–Padgett Regional", "code": "USA"},
        {"name": "Rocky Mount–Wilson Regional", "code": "RWI"},
    ]
    return jsonify(nc_airports)


@app.route("/api/flights")
@login_required
def api_flights():
    """
    Returns flights.
    If ?airport=CODE is given, filters flights for that airport.
    """
    airport_code = request.args.get("airport")

    # Example static data (you can replace this with FlightAware or AirLabs API)
    all_flights = [
        {"flight": "AA123", "from": "CLT", "to": "RDU", "dep": "2025-11-08T14:00:00", "arr": "2025-11-08T14:45:00"},
        {"flight": "DL456", "from": "RDU", "to": "ATL", "dep": "2025-11-08T15:30:00", "arr": "2025-11-08T17:00:00"},
        {"flight": "UA789", "from": "GSO", "to": "ORD", "dep": "2025-11-08T13:00:00", "arr": "2025-11-08T14:30:00"},
        {"flight": "WN999", "from": "CLT", "to": "TPA", "dep": "2025-11-08T16:00:00", "arr": "2025-11-08T18:00:00"},
        {"flight": "AA345", "from": "AVL", "to": "DCA", "dep": "2025-11-08T12:00:00", "arr": "2025-11-08T13:45:00"},
    ]

    if airport_code:
        flights = [f for f in all_flights if f["from"] == airport_code or f["to"] == airport_code]
    else:
        flights = all_flights

    return jsonify(flights)


if __name__ == "__main__":
    app.run(debug=True)
