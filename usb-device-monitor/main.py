"""
USBLOCKR - USB Physical Security Tool
Supraja Technologies | Cyber Security Internship
Developer: Rajkumar Kalapala (ST#IS#0000)
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import os
import sys
import threading
import subprocess

# ── colour palette (matrix / hacker theme) ────────────────────────────────────
BG       = "#0a0a0a"
GREEN    = "#00ff41"
GREEN_DK = "#006400"
RED      = "#cc0000"
RED_LT   = "#ff1a1a"
GREY     = "#1a1a1a"
MONO     = ("Courier New", 11)
MONO_LG  = ("Courier New", 18, "bold")
MONO_SM  = ("Courier New", 9)

# ── lazy imports (so app starts even if optional libs missing) ─────────────────
def try_import(name):
    try:
        return __import__(name)
    except ImportError:
        return None

cv2   = try_import("cv2")
PIL   = try_import("PIL")

from core.usb_controller  import disable_usb, enable_usb, get_usb_status
from core.snapshot        import take_snapshot, SNAPSHOT_DIR
from core.password_gen    import generate_password
from core.email_sender    import send_alert_email
from core.usb_monitor     import USBMonitor
from core.whitelist       import WhitelistManager
from database.db_manager  import DBManager


# ══════════════════════════════════════════════════════════════════════════════
class USBLockrApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # ── window setup ──────────────────────────────────────────────────────
        self.title("USBLOCKR")
        self.geometry("900x620")
        self.configure(bg=BG)
        self.resizable(False, False)

        # ── state ─────────────────────────────────────────────────────────────
        self.db           = DBManager()
        self.whitelist_mgr= WhitelistManager(self.db)
        self.usb_monitor  = USBMonitor(on_new_device=self._on_usb_event)
        self.current_user = None          # set after login
        self.usb_enabled  = get_usb_status()

        # ── build UI ──────────────────────────────────────────────────────────
        self._build_logo_bar()
        self._build_main_panel()
        self._build_status_bar()

        # ── start USB monitor ─────────────────────────────────────────────────
        self.usb_monitor.start()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # ── login prompt ──────────────────────────────────────────────────────
        self.after(300, self._show_login)

    # ── TOP BAR (logo + project report button) ─────────────────────────────────
    def _build_logo_bar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=16, pady=(12, 0))

        # logo text (replace with image if you have logo.png)
        logo_frame = tk.Frame(bar, bg=BG)
        logo_frame.pack(side="left")
        canvas = tk.Canvas(logo_frame, width=56, height=56,
                           bg=BG, highlightthickness=0)
        canvas.pack(side="left")
        self._draw_logo(canvas)
        tk.Label(logo_frame, text="USBLOCKR", font=("Courier New", 13, "bold"),
                 fg=GREEN, bg=BG).pack(side="left", padx=(4, 0), anchor="s")

        # project report button (top-right, matches Image 6)
        btn = tk.Button(bar, text="ℹ  Project Report",
                        font=MONO_SM, fg=GREEN, bg=BG,
                        activeforeground=BG, activebackground=GREEN,
                        relief="solid", bd=1, cursor="hand2",
                        highlightcolor=GREEN, highlightbackground=GREEN,
                        command=self._show_project_info)
        btn.pack(side="right", ipadx=8, ipady=4)

    def _draw_logo(self, canvas):
        """Draw a simple shield+U logo matching the USBLOCKR icon in Image 6."""
        c = canvas
        # shield body
        c.create_polygon(28,4, 52,14, 52,34, 28,52, 4,34, 4,14,
                         fill="#003300", outline=GREEN, width=2)
        # letter U
        c.create_text(28, 30, text="U", font=("Courier New", 18, "bold"),
                      fill=GREEN)
        # circuit dots
        for x, y in [(10,10),(46,10),(10,44),(46,44)]:
            c.create_oval(x-2,y-2,x+2,y+2, fill=GREEN, outline="")

    # ── MAIN PANEL ─────────────────────────────────────────────────────────────
    def _build_main_panel(self):
        self.main_frame = tk.Frame(self, bg=BG)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=8)

        # title
        tk.Label(self.main_frame,
                 text="🔒  USB Security Dashboard",
                 font=MONO_LG, fg=GREEN, bg=BG).pack(pady=(12, 4))

        # status indicator
        self.status_var = tk.StringVar()
        self._refresh_status_label()
        self.status_lbl = tk.Label(self.main_frame,
                                   textvariable=self.status_var,
                                   font=MONO, bg=BG, fg=GREEN)
        self.status_lbl.pack(pady=(0, 18))

        # ── top two big buttons (Disable / Enable) ────────────────────────────
        row1 = tk.Frame(self.main_frame, bg=BG)
        row1.pack(fill="x", pady=(0, 10))

        self.btn_disable = tk.Button(
            row1, text="✘  Disable Port",
            font=("Courier New", 13, "bold"),
            fg="white", bg=RED, activebackground=RED_LT,
            activeforeground="white", relief="flat", cursor="hand2",
            command=self._disable_usb)
        self.btn_disable.pack(side="left", expand=True, fill="x",
                              ipady=14, padx=(0, 6))

        self.btn_enable = tk.Button(
            row1, text="☑  Enable Port",
            font=("Courier New", 13, "bold"),
            fg="white", bg=GREEN_DK, activebackground="#00aa00",
            activeforeground="white", relief="flat", cursor="hand2",
            command=self._enable_usb)
        self.btn_enable.pack(side="right", expand=True, fill="x",
                             ipady=14, padx=(6, 0))

        # ── secondary action buttons ──────────────────────────────────────────
        actions = [
            ("📷  Take Snapshot Now (Test)",  self._take_snapshot),
            ("📂  Open Snapshots Folder",      self._open_snapshots),
            ("📋  Show Logs",                  self._show_logs),
        ]
        for label, cmd in actions:
            b = tk.Button(self.main_frame, text=label,
                          font=MONO, fg=GREEN, bg=GREY,
                          activeforeground=BG, activebackground=GREEN,
                          relief="flat", cursor="hand2",
                          bd=0, highlightthickness=1,
                          highlightcolor=GREEN,
                          highlightbackground=GREEN,
                          command=cmd)
            b.pack(fill="x", ipady=11, pady=3)

        # ── admin-only extras (password gen, whitelist, user mgmt) ────────────
        self.admin_frame = tk.Frame(self.main_frame, bg=BG)
        self.admin_frame.pack(fill="x", pady=(8, 0))

        admin_btns = [
            ("🔑  Generate OTP & Email Alert",   self._gen_password_email),
            ("🛡  Manage USB Whitelist",           self._manage_whitelist),
            ("👤  User Management (Admin)",        self._user_management),
        ]
        for label, cmd in admin_btns:
            b = tk.Button(self.admin_frame, text=label,
                          font=MONO_SM, fg="#aaffaa", bg=BG,
                          activeforeground=BG, activebackground=GREEN,
                          relief="solid", bd=1, cursor="hand2",
                          highlightcolor=GREEN, highlightbackground=GREEN,
                          command=cmd)
            b.pack(fill="x", ipady=6, pady=2)

        # hidden until logged-in as admin
        self.admin_frame.pack_forget()

    # ── STATUS BAR ─────────────────────────────────────────────────────────────
    def _build_status_bar(self):
        bar = tk.Frame(self, bg="#111", bd=1, relief="sunken")
        bar.pack(fill="x", side="bottom")
        self.statusbar_var = tk.StringVar(value="Ready")
        tk.Label(bar, textvariable=self.statusbar_var,
                 font=MONO_SM, fg="#666", bg="#111",
                 anchor="w").pack(side="left", padx=8, pady=2)

    def _set_status(self, msg):
        self.statusbar_var.set(msg)

    def _refresh_status_label(self):
        if self.usb_enabled:
            self.status_var.set("☑  USB Ports ENABLED")
        else:
            self.status_var.set("⊠  USB Ports DISABLED")

    # ══════════════════════════════════════════════════════════════════════════
    # LOGIN
    # ══════════════════════════════════════════════════════════════════════════
    def _show_login(self):
        from gui.login_window import LoginWindow
        LoginWindow(self, self.db, callback=self._on_login_success)

    def _on_login_success(self, user_record):
        self.current_user = user_record
        role = user_record["role"]
        self._set_status(f"Logged in as: {user_record['username']}  [{role}]")
        if role == "admin":
            self.admin_frame.pack(fill="x", pady=(8, 0))

    # ══════════════════════════════════════════════════════════════════════════
    # USB CONTROLS
    # ══════════════════════════════════════════════════════════════════════════
    def _disable_usb(self):
        if not self._check_login():
            return
        ok, msg = disable_usb()
        if ok:
            self.usb_enabled = False
            self._refresh_status_label()
            self._log_action("USB Ports DISABLED")
            self._set_status("USB ports disabled successfully.")
            messagebox.showinfo("USBLOCKR", "✔ USB Ports have been DISABLED.")
        else:
            messagebox.showerror("Error", msg)

    def _enable_usb(self):
        if not self._check_login():
            return
        ok, msg = enable_usb()
        if ok:
            self.usb_enabled = True
            self._refresh_status_label()
            self._log_action("USB Ports ENABLED")
            self._set_status("USB ports enabled successfully.")
            messagebox.showinfo("USBLOCKR", "✔ USB Ports have been ENABLED.")
        else:
            messagebox.showerror("Error", msg)

    # ══════════════════════════════════════════════════════════════════════════
    # SNAPSHOT
    # ══════════════════════════════════════════════════════════════════════════
    def _take_snapshot(self):
        def _run():
            path, err = take_snapshot()
            if path:
                self._log_action(f"Snapshot saved: {path}")
                self._set_status(f"Snapshot saved → {path}")
                messagebox.showinfo("Snapshot", f"✔ Snapshot saved!\n{path}")
            else:
                messagebox.showerror("Snapshot Error", err)
        threading.Thread(target=_run, daemon=True).start()

    def _open_snapshots(self):
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        os.startfile(SNAPSHOT_DIR)

    # ══════════════════════════════════════════════════════════════════════════
    # LOGS
    # ══════════════════════════════════════════════════════════════════════════
    def _show_logs(self):
        from gui.log_viewer import LogViewer
        LogViewer(self)

    def _log_action(self, action):
        self.db.add_log(
            user=self.current_user["username"] if self.current_user else "system",
            action=action
        )

    # ══════════════════════════════════════════════════════════════════════════
    # PASSWORD GENERATION + EMAIL
    # ══════════════════════════════════════════════════════════════════════════
    def _gen_password_email(self):
        from gui.email_dialog import EmailDialog
        EmailDialog(self, self.db)

    # ══════════════════════════════════════════════════════════════════════════
    # WHITELIST
    # ══════════════════════════════════════════════════════════════════════════
    def _manage_whitelist(self):
        from gui.whitelist_window import WhitelistWindow
        WhitelistWindow(self, self.whitelist_mgr)

    # ══════════════════════════════════════════════════════════════════════════
    # USER MANAGEMENT (admin only)
    # ══════════════════════════════════════════════════════════════════════════
    def _user_management(self):
        from gui.user_mgmt import UserMgmtWindow
        UserMgmtWindow(self, self.db)

    # ══════════════════════════════════════════════════════════════════════════
    # PROJECT INFO (matches Image 2)
    # ══════════════════════════════════════════════════════════════════════════
    def _show_project_info(self):
        from gui.project_info import ProjectInfoWindow
        ProjectInfoWindow(self)

    # ══════════════════════════════════════════════════════════════════════════
    # USB MONITOR CALLBACK
    # ══════════════════════════════════════════════════════════════════════════
    def _on_usb_event(self, device_id):
        """Called by USBMonitor thread when a new USB device is inserted."""
        allowed = self.whitelist_mgr.is_allowed(device_id)
        self._log_action(f"USB inserted: {device_id} | allowed={allowed}")
        if not allowed:
            # take snapshot of intruder
            path, _ = take_snapshot()
            snap_note = f" Snapshot: {path}" if path else ""
            self._set_status(f"⚠ Unauthorised USB! {device_id}{snap_note}")
            # send alert email in background
            threading.Thread(
                target=send_alert_email,
                args=(device_id, path),
                daemon=True
            ).start()
            self.after(0, lambda: messagebox.showwarning(
                "⚠ ALERT – Unauthorised USB",
                f"Unknown device detected!\n{device_id}\n"
                f"Snapshot captured & alert email sent.{snap_note}"
            ))

    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════════════════
    def _check_login(self):
        if self.current_user is None:
            messagebox.showwarning("Login Required", "Please log in first.")
            self._show_login()
            return False
        return True

    def _on_close(self):
        self.usb_monitor.stop()
        self.destroy()


# ── entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = USBLockrApp()
    app.mainloop()
