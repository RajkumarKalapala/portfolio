"""
database.py
-----------
SQLite database manager for:
  - Activity logs
  - Privacy schedules
  - User accounts (Admin / User roles)
"""

import sqlite3
import os
import hashlib
import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webcam_security.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist and seed default admin."""
    conn = get_connection()
    cur = conn.cursor()

    # ── Users table ──────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            role        TEXT    NOT NULL DEFAULT 'User',
            email       TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── Logs table ───────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL,
            action      TEXT    NOT NULL,
            details     TEXT,
            user        TEXT    DEFAULT 'System'
        )
    """)

    # ── Privacy schedules table ──────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time  TEXT    NOT NULL,
            end_time    TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'Active',
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── Registered faces table ───────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registered_faces (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            image_path  TEXT    NOT NULL,
            registered_at TEXT  DEFAULT (datetime('now'))
        )
    """)

    # Seed default admin if none exists
    cur.execute("SELECT COUNT(*) FROM users WHERE role='Admin'")
    if cur.fetchone()[0] == 0:
        admin_pass = hash_password("Admin@123")
        cur.execute(
            "INSERT INTO users (username, password, role, email) VALUES (?,?,?,?)",
            ("admin", admin_pass, "Admin", "admin@supraja.com")
        )

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── User operations ──────────────────────────────────────────────────────────

def verify_user(username: str, password: str):
    """Returns user row if credentials match, else None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    row = cur.fetchone()
    conn.close()
    return row


def add_user(username: str, password: str, role: str = "User", email: str = "") -> tuple[bool, str]:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password, role, email) VALUES (?,?,?,?)",
            (username, hash_password(password), role, email)
        )
        conn.commit()
        conn.close()
        return True, f"User '{username}' added successfully."
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' already exists."
    except Exception as e:
        return False, str(e)


def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role, email, created_at FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows


def change_password(username: str, old_password: str, new_password: str) -> tuple[bool, str]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, hash_password(old_password))
    )
    if not cur.fetchone():
        conn.close()
        return False, "Incorrect current password."
    cur.execute(
        "UPDATE users SET password=? WHERE username=?",
        (hash_password(new_password), username)
    )
    conn.commit()
    conn.close()
    return True, "Password changed successfully."


# ── Log operations ───────────────────────────────────────────────────────────

def add_log(action: str, details: str = "", user: str = "System"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (timestamp, action, details, user) VALUES (?,?,?,?)",
        (timestamp, action, details, user)
    )
    conn.commit()
    conn.close()


def get_logs(limit: int = 200):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT timestamp, action, details, user FROM logs ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def clear_logs():
    conn = get_connection()
    conn.execute("DELETE FROM logs")
    conn.commit()
    conn.close()


# ── Schedule operations ──────────────────────────────────────────────────────

def add_schedule(start_time: str, end_time: str) -> tuple[bool, str]:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO schedules (start_time, end_time, status) VALUES (?,?,?)",
            (start_time, end_time, "Active")
        )
        conn.commit()
        conn.close()
        return True, "Schedule added."
    except Exception as e:
        return False, str(e)


def get_schedules():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, start_time, end_time, status FROM schedules ORDER BY start_time")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_schedule(schedule_id: int, start_time: str, end_time: str, status: str) -> tuple[bool, str]:
    try:
        conn = get_connection()
        conn.execute(
            "UPDATE schedules SET start_time=?, end_time=?, status=? WHERE id=?",
            (start_time, end_time, status, schedule_id)
        )
        conn.commit()
        conn.close()
        return True, "Schedule updated."
    except Exception as e:
        return False, str(e)


def delete_schedule(schedule_id: int) -> tuple[bool, str]:
    try:
        conn = get_connection()
        conn.execute("DELETE FROM schedules WHERE id=?", (schedule_id,))
        conn.commit()
        conn.close()
        return True, "Schedule deleted."
    except Exception as e:
        return False, str(e)


def get_active_schedules():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, start_time, end_time FROM schedules WHERE status='Active'")
    rows = cur.fetchall()
    conn.close()
    return rows


# ── Face registration ────────────────────────────────────────────────────────

def register_face(name: str, image_path: str) -> tuple[bool, str]:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO registered_faces (name, image_path) VALUES (?,?)",
            (name, image_path)
        )
        conn.commit()
        conn.close()
        return True, f"Face registered for '{name}'."
    except Exception as e:
        return False, str(e)


def get_registered_faces():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, image_path, registered_at FROM registered_faces")
    rows = cur.fetchall()
    conn.close()
    return rows
