"""
database/db_manager.py
SQLite database for USBLOCKR.
Tables: users, logs, whitelist, smtp_config
"""

import sqlite3
import os
import hashlib
import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                       "database", "usblockr.db")


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class DBManager:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._init_db()

    def _conn(self):
        return sqlite3.connect(DB_PATH)

    def _init_db(self):
        with self._conn() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT    UNIQUE NOT NULL,
                    password TEXT    NOT NULL,
                    role     TEXT    NOT NULL DEFAULT 'user',
                    email    TEXT    DEFAULT ''
                );

                CREATE TABLE IF NOT EXISTS logs (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT    NOT NULL,
                    username  TEXT    NOT NULL,
                    action    TEXT    NOT NULL
                );

                CREATE TABLE IF NOT EXISTS whitelist (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT    UNIQUE NOT NULL,
                    label     TEXT    DEFAULT '',
                    added_at  TEXT    NOT NULL
                );

                CREATE TABLE IF NOT EXISTS smtp_config (
                    id        INTEGER PRIMARY KEY,
                    host      TEXT DEFAULT 'smtp.gmail.com',
                    port      INTEGER DEFAULT 587,
                    username  TEXT DEFAULT '',
                    password  TEXT DEFAULT '',
                    alert_to  TEXT DEFAULT ''
                );
            """)
            # seed default admin if no users exist
            cur = c.execute("SELECT COUNT(*) FROM users")
            if cur.fetchone()[0] == 0:
                c.execute(
                    "INSERT INTO users (username, password, role, email) "
                    "VALUES (?, ?, ?, ?)",
                    ("admin", _hash("admin123"), "admin", "admin@example.com")
                )
                c.execute(
                    "INSERT INTO users (username, password, role, email) "
                    "VALUES (?, ?, ?, ?)",
                    ("user1", _hash("user123"), "user", "user@example.com")
                )

    # ── USER ──────────────────────────────────────────────────────────────────
    def authenticate(self, username: str, password: str):
        """Return user dict or None."""
        with self._conn() as c:
            c.row_factory = sqlite3.Row
            cur = c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, _hash(password))
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def add_user(self, username, password, role="user", email=""):
        try:
            with self._conn() as c:
                c.execute(
                    "INSERT INTO users (username, password, role, email) "
                    "VALUES (?,?,?,?)",
                    (username, _hash(password), role, email)
                )
            return True, "User created."
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    def delete_user(self, username):
        with self._conn() as c:
            c.execute("DELETE FROM users WHERE username=?", (username,))
        return True, "Deleted."

    def list_users(self):
        with self._conn() as c:
            c.row_factory = sqlite3.Row
            rows = c.execute(
                "SELECT id, username, role, email FROM users ORDER BY id"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_user_email(self, username: str) -> str:
        with self._conn() as c:
            cur = c.execute("SELECT email FROM users WHERE username=?", (username,))
            r = cur.fetchone()
            return r[0] if r else ""

    # ── LOGS ──────────────────────────────────────────────────────────────────
    def add_log(self, user: str, action: str):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._conn() as c:
            c.execute(
                "INSERT INTO logs (timestamp, username, action) VALUES (?,?,?)",
                (ts, user, action)
            )

    def get_logs(self, limit: int = 200) -> list:
        with self._conn() as c:
            c.row_factory = sqlite3.Row
            rows = c.execute(
                "SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    # ── WHITELIST ─────────────────────────────────────────────────────────────
    def get_whitelist(self) -> set:
        with self._conn() as c:
            rows = c.execute("SELECT device_id FROM whitelist").fetchall()
            return {r[0] for r in rows}

    def get_whitelist_full(self) -> list:
        with self._conn() as c:
            c.row_factory = sqlite3.Row
            rows = c.execute("SELECT * FROM whitelist ORDER BY id").fetchall()
            return [dict(r) for r in rows]

    def add_to_whitelist(self, device_id: str, label: str = "") -> bool:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self._conn() as c:
                c.execute(
                    "INSERT INTO whitelist (device_id, label, added_at) "
                    "VALUES (?,?,?)",
                    (device_id, label, ts)
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_from_whitelist(self, device_id: str) -> bool:
        with self._conn() as c:
            c.execute("DELETE FROM whitelist WHERE device_id=?", (device_id,))
        return True

    # ── SMTP CONFIG ───────────────────────────────────────────────────────────
    def get_smtp(self) -> dict:
        with self._conn() as c:
            c.row_factory = sqlite3.Row
            row = c.execute("SELECT * FROM smtp_config WHERE id=1").fetchone()
            if row:
                return dict(row)
            return {}

    def save_smtp(self, host, port, username, password, alert_to):
        with self._conn() as c:
            c.execute("DELETE FROM smtp_config")
            c.execute(
                "INSERT INTO smtp_config (id,host,port,username,password,alert_to) "
                "VALUES (1,?,?,?,?,?)",
                (host, int(port), username, password, alert_to)
            )
