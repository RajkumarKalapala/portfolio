"""
main.py  –  Webcam Spyware Security System
Supraja Technologies  |  Cyber Security Internship Project
----------------------------------------------------------
Matches the UI shown in the project screenshots:
  • Dark theme (charcoal background)
  • Header: webcam icon + title + status (red text)
  • Buttons: Enable Camera (green), Disable Camera (red),
             Register Face (purple), View Logs (blue)
  • Privacy Schedules treeview + Add / Edit / Delete
  • Project Info popup
  • Password-protected operations
  • Face recognition enrollment via OpenCV
  • Background scheduler thread
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
import threading
import datetime
import random
import string
import smtplib
from email.mime.text import MIMEText

# ── Local modules ─────────────────────────────────────────────────────────────
from database import (
    init_db, add_log, get_logs, clear_logs,
    add_schedule, get_schedules, update_schedule, delete_schedule,
    verify_user, add_user, change_password, get_all_users,
    register_face, get_registered_faces, hash_password
)
# from camera_control import (
#     enable_camera, disable_camera, get_camera_status, is_admin, request_admin
# )
from camera_control import (
    enable_camera,
    disable_camera,
    is_camera_enabled,
    is_admin,
    request_admin
)

from scheduler import PrivacyScheduler

# ── Optional dependencies ─────────────────────────────────────────────────────
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import face_recognition
    FACE_REC_AVAILABLE = True
except ImportError:
    FACE_REC_AVAILABLE = False

# ─────────────────────────────────────────────────────────────────────────────
#  COLOURS  (matching the dark theme in the screenshots)
# ─────────────────────────────────────────────────────────────────────────────
BG_DARK        = "#1e1e1e"
BG_PANEL       = "#2a2a2a"
BG_HEADER      = "#1e1e1e"
FG_WHITE       = "#ffffff"
FG_RED         = "#ff4444"
FG_GREEN       = "#44ff44"
FG_GRAY        = "#aaaaaa"

BTN_GREEN      = "#28a745"
BTN_GREEN_HOV  = "#218838"
BTN_RED        = "#dc3545"
BTN_RED_HOV    = "#c82333"
BTN_PURPLE     = "#6f42c1"
BTN_PURPLE_HOV = "#5a32a3"
BTN_BLUE       = "#007bff"
BTN_BLUE_HOV   = "#0069d9"
BTN_YELLOW     = "#e0a800"
BTN_YELLOW_HOV = "#c69500"
BTN_GRAY       = "#6c757d"
BTN_GRAY_HOV   = "#5a6268"

TREE_BG        = "#252525"
TREE_FG        = "#dddddd"
TREE_SEL       = "#3a3a5c"
TREE_HEADING   = "#333333"

# ─────────────────────────────────────────────────────────────────────────────
#  PROJECT INFORMATION  (matches Image 7)
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_INFO = {
    "name"        : "Web Cam Security from Spyware",
    "description" : "Implementing Physical Security Policy on Web Cam in Devices to Prevent Spyware Activities",
    "start_date"  : "01-DEC-2025",
    "end_date"    : "31-DEC-2025",
    "status"      : "Completed",
    "developer"   : "Anonymous",
    "emp_id"      : "ST#IS#0000",
    "dev_email"   : "anonymous@gmail.com",
    "company"     : "Supraja Technologies",
    "company_email": "contact@suprajatechnologies.com",
    "website"     : "https://suprajatechnologies.com",
}

CURRENT_USER = {"username": "admin", "role": "Admin"}  # set on login


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER: rounded / hover buttons
# ─────────────────────────────────────────────────────────────────────────────
def make_button(parent, text, command, bg, fg="#ffffff",
                hov=None, width=14, font_size=10, padx=10, pady=6):
    hov = hov or bg
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, activebackground=hov, activeforeground=fg,
        relief="flat", cursor="hand2",
        font=("Segoe UI", font_size, "bold"),
        width=width, padx=padx, pady=pady,
        bd=0
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hov))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
class WebcamSecurityApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # ── Window setup ─────────────────────────────────────────────────────
        self.title("Webcam Spyware Security System - Supraja Technologies")
        self.configure(bg=BG_DARK)
        self.geometry("900x640")
        self.minsize(760, 560)

        # Webcam icon (uses Unicode fallback if PIL not available)
        try:
            self.iconbitmap(default="")   # clear default
        except Exception:
            pass

        # ── DB init ──────────────────────────────────────────────────────────
        init_db()

        # ── Scheduler ────────────────────────────────────────────────────────
        self.scheduler = PrivacyScheduler(status_callback=self._on_scheduler_event)
        self.scheduler.start()

        # ── Build UI ─────────────────────────────────────────────────────────
        self._build_ui()
        self._refresh_status()
        self._refresh_schedules()

        # ── Periodic status refresh (every 5 s) ───────────────────────────────
        self._schedule_status_refresh()

        # ── Log startup ──────────────────────────────────────────────────────
        add_log("Startup", "Application started", CURRENT_USER["username"])

    # ─────────────────────────────────────────────────────────────────────────
    #  UI CONSTRUCTION
    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Top bar: Project Info button ─────────────────────────────────────
        top_bar = tk.Frame(self, bg=BG_DARK)
        top_bar.pack(fill="x", pady=(8, 0), padx=10)

        make_button(top_bar, "Project Info", self._show_project_info,
                    bg=BTN_GRAY, hov=BTN_GRAY_HOV, width=12, font_size=9
                    ).pack(side="left")

        # ── Header: icon + title ─────────────────────────────────────────────
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(8, 0))

        # Webcam icon (canvas drawn)
        icon_canvas = tk.Canvas(header, width=48, height=48,
                                bg=BG_DARK, highlightthickness=0)
        icon_canvas.pack(side="left")
        self._draw_webcam_icon(icon_canvas)

        tk.Label(header, text="Webcam Spyware Security System",
                 font=("Segoe UI", 18, "bold"),
                 fg=FG_WHITE, bg=BG_DARK).pack(side="left", padx=10)

        # ── Status label ─────────────────────────────────────────────────────
        status_frame = tk.Frame(self, bg=BG_DARK)
        status_frame.pack(fill="x", padx=16, pady=(4, 0))
        self.status_var = tk.StringVar(value="Webcam Status: Loading...")
        self.status_label = tk.Label(
            status_frame, textvariable=self.status_var,
            font=("Segoe UI", 11, "bold"),
            fg=FG_RED, bg=BG_DARK
        )
        self.status_label.pack(side="left")

        # ── Action buttons row ───────────────────────────────────────────────
        btn_row = tk.Frame(self, bg=BG_DARK)
        btn_row.pack(fill="x", padx=16, pady=12)

        self.btn_enable = make_button(
            btn_row, "Enable Camera", self._enable_camera,
            BTN_GREEN, hov=BTN_GREEN_HOV, width=14)
        self.btn_enable.pack(side="left", padx=(0, 6))

        self.btn_disable = make_button(
            btn_row, "Disable Camera", self._disable_camera,
            BTN_RED, hov=BTN_RED_HOV, width=14)
        self.btn_disable.pack(side="left", padx=(0, 6))

        make_button(btn_row, "Register Face", self._register_face,
                    BTN_PURPLE, hov=BTN_PURPLE_HOV, width=14
                    ).pack(side="left", padx=(0, 6))

        make_button(btn_row, "View Logs", self._view_logs,
                    BTN_BLUE, hov=BTN_BLUE_HOV, width=12
                    ).pack(side="left")

        # ── Privacy Schedules section ─────────────────────────────────────────
        sched_lbl = tk.Label(
            self,
            text="Privacy Schedules (Auto-blocks webcam during specified times)",
            font=("Segoe UI", 10), fg=FG_GRAY, bg=BG_DARK
        )
        sched_lbl.pack(pady=(0, 2))

        # Treeview
        tree_frame = tk.Frame(self, bg=BG_DARK)
        tree_frame.pack(fill="both", expand=True, padx=16)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.Treeview",
                        background=TREE_BG,
                        foreground=TREE_FG,
                        fieldbackground=TREE_BG,
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Dark.Treeview.Heading",
                        background=TREE_HEADING,
                        foreground=FG_WHITE,
                        font=("Segoe UI", 10, "bold"),
                        relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", TREE_SEL)],
                  foreground=[("selected", FG_WHITE)])

        cols = ("Start Time", "End Time", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=cols,
                                 show="headings", style="Dark.Treeview")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center",
                             width=200 if col != "Status" else 120)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # ── Bottom schedule buttons ───────────────────────────────────────────
        bottom_bar = tk.Frame(self, bg=BG_DARK)
        bottom_bar.pack(fill="x", padx=16, pady=10)

        make_button(bottom_bar, "Add Schedule", self._add_schedule,
                    BTN_GREEN, hov=BTN_GREEN_HOV, width=14
                    ).pack(side="left", padx=(0, 6))

        make_button(bottom_bar, "Edit Selected", self._edit_schedule,
                    BTN_YELLOW, fg="#000000", hov=BTN_YELLOW_HOV, width=14
                    ).pack(side="left", padx=(0, 6))

        make_button(bottom_bar, "Delete Selected", self._delete_schedule,
                    BTN_RED, hov=BTN_RED_HOV, width=14
                    ).pack(side="left")

    # ─────────────────────────────────────────────────────────────────────────
    #  WEBCAM ICON (drawn on canvas)
    # ─────────────────────────────────────────────────────────────────────────
    def _draw_webcam_icon(self, canvas):
        """Draw a simple webcam icon using canvas shapes."""
        # Body
        canvas.create_rectangle(4, 10, 44, 36, fill="#555555", outline="#888888", width=1)
        # Lens ring
        canvas.create_oval(14, 14, 34, 32, fill="#222222", outline="#aaaaaa", width=2)
        # Lens center
        canvas.create_oval(19, 19, 29, 29, fill="#0080ff", outline="")
        # Highlight dot
        canvas.create_oval(21, 21, 24, 24, fill="#80c8ff", outline="")
        # Stand
        canvas.create_rectangle(18, 36, 30, 42, fill="#555555", outline="")
        canvas.create_rectangle(12, 42, 36, 46, fill="#666666", outline="")

    # ─────────────────────────────────────────────────────────────────────────
    #  STATUS REFRESH
    # ─────────────────────────────────────────────────────────────────────────
    # def _refresh_status(self):
    #     status = get_camera_status()
    #     if status.lower() == "allow":
    #         self.status_var.set("Webcam Status: Enable")
    #         self.status_label.config(fg="#44ff44")
    #     elif status.lower() == "deny":
    #         self.status_var.set("Webcam Status: Disable")
    #         self.status_label.config(fg=FG_RED)
    #     else:
    #         self.status_var.set(f"Webcam Status: {status}")
    #         self.status_label.config(fg="#ffaa00")
    def _refresh_status(self):
        if is_camera_enabled():
            self.status_var.set("Webcam Status: Enabled")
            self.status_label.config(fg="#44ff44")
        else:
            self.status_var.set("Webcam Status: Disabled")
            self.status_label.config(fg=FG_RED)

    def _schedule_status_refresh(self):
        self._refresh_status()
        self.after(5000, self._schedule_status_refresh)

    def _on_scheduler_event(self, event: str):
        """Called from scheduler thread when camera state changes."""
        if event == "disabled_by_schedule":
            self.after(0, self._refresh_status)

    # ─────────────────────────────────────────────────────────────────────────
    #  CAMERA OPERATIONS
    # ─────────────────────────────────────────────────────────────────────────
    def _enable_camera(self):
        if not is_admin():
            messagebox.showerror(
                "Admin Required",
                "This operation requires Administrator privileges.\n"
                "Please run the application as Administrator."
            )
            return
        ok, msg = enable_camera()
        if ok:
            add_log("Enable Camera", msg, CURRENT_USER["username"])
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
        self._refresh_status()

    def _disable_camera(self):
        if not is_admin():
            messagebox.showerror(
                "Admin Required",
                "This operation requires Administrator privileges.\n"
                "Please run the application as Administrator."
            )
            return
        ok, msg = disable_camera()
        if ok:
            add_log("Disable Camera", msg, CURRENT_USER["username"])
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
        self._refresh_status()

    # ─────────────────────────────────────────────────────────────────────────
    #  FACE REGISTRATION
    # ─────────────────────────────────────────────────────────────────────────
    def _register_face(self):
        if not CV2_AVAILABLE:
            messagebox.showwarning(
                "OpenCV Missing",
                "OpenCV (cv2) is not installed.\n"
                "Install it with: pip install opencv-python"
            )
            return

        name = simpledialog.askstring("Register Face",
                                      "Enter the person's name:",
                                      parent=self)
        if not name or not name.strip():
            return
        name = name.strip()

        FaceRegistrationDialog(self, name)

    # ─────────────────────────────────────────────────────────────────────────
    #  LOGS VIEWER
    # ─────────────────────────────────────────────────────────────────────────
    def _view_logs(self):
        LogViewerWindow(self)

    # ─────────────────────────────────────────────────────────────────────────
    #  SCHEDULE OPERATIONS
    # ─────────────────────────────────────────────────────────────────────────
    def _refresh_schedules(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for s in get_schedules():
            self.tree.insert("", "end",
                             iid=str(s["id"]),
                             values=(s["start_time"], s["end_time"], s["status"]))

    def _add_schedule(self):
        ScheduleDialog(self, mode="add", on_save=self._refresh_schedules)

    def _edit_schedule(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a schedule to edit.")
            return
        values = self.tree.item(selected, "values")
        ScheduleDialog(self, mode="edit",
                       schedule_id=int(selected),
                       current_values=values,
                       on_save=self._refresh_schedules)

    def _delete_schedule(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a schedule to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete",
                                      "Delete the selected schedule?")
        if confirm:
            ok, msg = delete_schedule(int(selected))
            if ok:
                add_log("Delete Schedule", f"Schedule {selected} deleted",
                        CURRENT_USER["username"])
                self._refresh_schedules()
            else:
                messagebox.showerror("Error", msg)

    # ─────────────────────────────────────────────────────────────────────────
    #  PROJECT INFO POPUP  (matches Image 7)
    # ─────────────────────────────────────────────────────────────────────────
    def _show_project_info(self):
        ProjectInfoWindow(self)


# ─────────────────────────────────────────────────────────────────────────────
#  PROJECT INFO WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class ProjectInfoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Project Information")
        self.configure(bg="white")
        self.geometry("680x580")
        self.resizable(False, False)
        self.grab_set()

        # ── Title ────────────────────────────────────────────────────────────
        tk.Label(self, text="Project Information",
                 font=("Segoe UI", 20, "bold"),
                 fg="#111111", bg="white"
                 ).pack(anchor="w", padx=30, pady=(24, 4))

        p = PROJECT_INFO
        intro = (
            f"This project was developed by Cyber ACE as part of a "
            f"Cyber Security Internship. This project is designed to "
            f"Secure the Organizations in Real World from Cyber Frauds "
            f"performed by Hackers."
        )
        tk.Label(self, text=intro, wraplength=600,
                 justify="left", font=("Segoe UI", 10),
                 bg="white", fg="#333333"
                 ).pack(anchor="w", padx=30, pady=(0, 10))

        # ── Tables helper ─────────────────────────────────────────────────────
        def make_table(parent, headers, rows):
            frame = tk.Frame(parent, bg="#cccccc", bd=1, relief="solid")
            frame.pack(fill="x", padx=30, pady=(0, 12))

            style = ttk.Style()
            style.configure("Info.Treeview",
                            background="white",
                            foreground="#222222",
                            rowheight=28,
                            font=("Segoe UI", 10))
            style.configure("Info.Treeview.Heading",
                            background="#e8e8e8",
                            foreground="#111111",
                            font=("Segoe UI", 10, "bold"))

            tv = ttk.Treeview(frame, columns=headers,
                              show="headings", style="Info.Treeview",
                              height=len(rows))
            for h in headers:
                tv.heading(h, text=h)
                tv.column(h, width=200, anchor="w")
            for r in rows:
                tv.insert("", "end", values=r)
            tv.pack(fill="x")

        # Project details table
        make_table(self,
                   ("Project Details", "Value"),
                   [
                       ("Project Name", p["name"]),
                       ("Project Description", p["description"]),
                       ("Project Start Date", p["start_date"]),
                       ("Project End Date", p["end_date"]),
                       ("Project Status", p["status"]),
                   ])

        tk.Label(self, text="Developer Details",
                 font=("Segoe UI", 13, "bold"),
                 bg="white", fg="#111111"
                 ).pack(anchor="w", padx=30, pady=(0, 4))

        make_table(self,
                   ("Name", "Employee ID", "Email"),
                   [(p["developer"], p["emp_id"], p["dev_email"])])

        tk.Label(self, text="Company Details",
                 font=("Segoe UI", 13, "bold"),
                 bg="white", fg="#111111"
                 ).pack(anchor="w", padx=30, pady=(0, 4))

        make_table(self,
                   ("Company", "Value"),
                   [
                       ("Name", p["company"]),
                       ("Email", p["company_email"]),
                       ("Website", p["website"]),
                   ])

        make_button(self, "Close", self.destroy,
                    BTN_RED, hov=BTN_RED_HOV, width=10
                    ).pack(pady=10)


# ─────────────────────────────────────────────────────────────────────────────
#  SCHEDULE DIALOG  (Add / Edit)
# ─────────────────────────────────────────────────────────────────────────────
class ScheduleDialog(tk.Toplevel):

    def __init__(self, parent, mode="add", schedule_id=None,
                 current_values=None, on_save=None):
        super().__init__(parent)
        self.mode = mode
        self.schedule_id = schedule_id
        self.on_save = on_save
        self.configure(bg=BG_DARK)
        self.title("Add Schedule" if mode == "add" else "Edit Schedule")
        self.geometry("380x260")
        self.resizable(False, False)
        self.grab_set()

        pad = {"padx": 20, "pady": 6}

        tk.Label(self, text="Start Time (HH:MM):",
                 fg=FG_WHITE, bg=BG_DARK,
                 font=("Segoe UI", 11)).pack(anchor="w", **pad)
        self.start_var = tk.StringVar()
        tk.Entry(self, textvariable=self.start_var,
                 font=("Segoe UI", 11), width=20
                 ).pack(anchor="w", padx=20)

        tk.Label(self, text="End Time (HH:MM):",
                 fg=FG_WHITE, bg=BG_DARK,
                 font=("Segoe UI", 11)).pack(anchor="w", **pad)
        self.end_var = tk.StringVar()
        tk.Entry(self, textvariable=self.end_var,
                 font=("Segoe UI", 11), width=20
                 ).pack(anchor="w", padx=20)

        if mode == "edit" and current_values:
            self.start_var.set(current_values[0])
            self.end_var.set(current_values[1])

        self.status_var = tk.StringVar(value="Active")
        if mode == "edit" and current_values and len(current_values) > 2:
            self.status_var.set(current_values[2])

        if mode == "edit":
            tk.Label(self, text="Status:",
                     fg=FG_WHITE, bg=BG_DARK,
                     font=("Segoe UI", 11)).pack(anchor="w", **pad)
            status_frame = tk.Frame(self, bg=BG_DARK)
            status_frame.pack(anchor="w", padx=20)
            for val in ("Active", "Inactive"):
                tk.Radiobutton(
                    status_frame, text=val, value=val,
                    variable=self.status_var,
                    bg=BG_DARK, fg=FG_WHITE,
                    selectcolor=BG_PANEL,
                    font=("Segoe UI", 10)
                ).pack(side="left", padx=6)

        btn_row = tk.Frame(self, bg=BG_DARK)
        btn_row.pack(pady=14)
        make_button(btn_row, "Save", self._save,
                    BTN_GREEN, hov=BTN_GREEN_HOV, width=8
                    ).pack(side="left", padx=6)
        make_button(btn_row, "Cancel", self.destroy,
                    BTN_GRAY, hov=BTN_GRAY_HOV, width=8
                    ).pack(side="left", padx=6)

    def _save(self):
        start = self.start_var.get().strip()
        end   = self.end_var.get().strip()

        # Validate HH:MM format
        for t in (start, end):
            try:
                datetime.datetime.strptime(t, "%H:%M")
            except ValueError:
                messagebox.showerror("Invalid Format",
                                     f"'{t}' is not a valid time. Use HH:MM (24-hour).",
                                     parent=self)
                return

        if self.mode == "add":
            ok, msg = add_schedule(start, end)
        else:
            ok, msg = update_schedule(
                self.schedule_id, start, end, self.status_var.get()
            )

        if ok:
            add_log(
                f"{'Add' if self.mode=='add' else 'Edit'} Schedule",
                f"{start}–{end}",
                CURRENT_USER["username"]
            )
            if self.on_save:
                self.on_save()
            self.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self)


# ─────────────────────────────────────────────────────────────────────────────
#  LOG VIEWER WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class LogViewerWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Activity Logs")
        self.configure(bg=BG_DARK)
        self.geometry("760x480")
        self.grab_set()

        tk.Label(self, text="Activity Logs",
                 font=("Segoe UI", 14, "bold"),
                 fg=FG_WHITE, bg=BG_DARK
                 ).pack(pady=(12, 4))

        frame = tk.Frame(self, bg=BG_DARK)
        frame.pack(fill="both", expand=True, padx=16, pady=6)

        style = ttk.Style()
        style.configure("Log.Treeview",
                        background=TREE_BG,
                        foreground=TREE_FG,
                        fieldbackground=TREE_BG,
                        rowheight=24,
                        font=("Consolas", 9))
        style.configure("Log.Treeview.Heading",
                        background=TREE_HEADING,
                        foreground=FG_WHITE,
                        font=("Segoe UI", 10, "bold"))
        style.map("Log.Treeview",
                  background=[("selected", TREE_SEL)])

        cols = ("Timestamp", "Action", "Details", "User")
        tree = ttk.Treeview(frame, columns=cols,
                            show="headings", style="Log.Treeview")
        tree.heading("Timestamp", text="Timestamp")
        tree.column("Timestamp", width=150, anchor="center")
        tree.heading("Action", text="Action")
        tree.column("Action", width=150, anchor="w")
        tree.heading("Details", text="Details")
        tree.column("Details", width=280, anchor="w")
        tree.heading("User", text="User")
        tree.column("User", width=100, anchor="center")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        for log in get_logs():
            tree.insert("", "end",
                        values=(log["timestamp"], log["action"],
                                log["details"], log["user"]))

        btn_row = tk.Frame(self, bg=BG_DARK)
        btn_row.pack(pady=8)

        def clear():
            if messagebox.askyesno("Clear Logs", "Clear all activity logs?",
                                   parent=self):
                clear_logs()
                for item in tree.get_children():
                    tree.delete(item)
                add_log("Clear Logs", "All logs cleared", CURRENT_USER["username"])

        make_button(btn_row, "Clear Logs", clear,
                    BTN_RED, hov=BTN_RED_HOV, width=10
                    ).pack(side="left", padx=6)
        make_button(btn_row, "Close", self.destroy,
                    BTN_GRAY, hov=BTN_GRAY_HOV, width=10
                    ).pack(side="left", padx=6)


# ─────────────────────────────────────────────────────────────────────────────
#  FACE REGISTRATION DIALOG
# ─────────────────────────────────────────────────────────────────────────────
class FaceRegistrationDialog(tk.Toplevel):

    def __init__(self, parent, name: str):
        super().__init__(parent)
        self.name = name
        self.configure(bg=BG_DARK)
        self.title(f"Register Face – {name}")
        self.geometry("500x420")
        self.grab_set()

        tk.Label(self, text=f"Registering face for: {name}",
                 font=("Segoe UI", 12, "bold"),
                 fg=FG_WHITE, bg=BG_DARK).pack(pady=(14, 4))

        tk.Label(self, text="Position face in front of webcam, then click Capture.",
                 font=("Segoe UI", 10), fg=FG_GRAY, bg=BG_DARK).pack()

        # Preview canvas
        self.canvas = tk.Canvas(self, width=320, height=240,
                                bg="#111111", highlightthickness=1,
                                highlightbackground="#555555")
        self.canvas.pack(pady=10)

        btn_row = tk.Frame(self, bg=BG_DARK)
        btn_row.pack(pady=6)

        self.btn_capture = make_button(btn_row, "Capture", self._capture,
                                       BTN_GREEN, hov=BTN_GREEN_HOV, width=10)
        self.btn_capture.pack(side="left", padx=6)

        make_button(btn_row, "Cancel", self._cancel,
                    BTN_RED, hov=BTN_RED_HOV, width=10
                    ).pack(side="left", padx=6)

        self.cap = None
        self.running = True
        self._start_preview()

    def _start_preview(self):
        if not CV2_AVAILABLE:
            return
        self.cap = cv2.VideoCapture(0)
        self._update_preview()

    def _update_preview(self):
        if not self.running or not self.cap:
            return
        ret, frame = self.cap.read()
        if ret and PIL_AVAILABLE:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb).resize((320, 240))
            self._photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self._photo)
        if self.running:
            self.after(30, self._update_preview)

    def _capture(self):
        if not self.cap:
            messagebox.showerror("Error", "Camera not accessible.", parent=self)
            return
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Could not capture frame.", parent=self)
            return

        # Save image
        faces_dir = os.path.join(os.path.dirname(__file__), "faces")
        os.makedirs(faces_dir, exist_ok=True)
        safe_name = "".join(c for c in self.name if c.isalnum() or c in " _-").strip()
        img_path = os.path.join(faces_dir, f"{safe_name}_{int(datetime.datetime.now().timestamp())}.jpg")
        cv2.imwrite(img_path, frame)

        ok, msg = register_face(self.name, img_path)
        if ok:
            add_log("Register Face", f"Face registered for '{self.name}'",
                    CURRENT_USER["username"])
            messagebox.showinfo("Success",
                                f"Face registered successfully for '{self.name}'!",
                                parent=self)
            self._cancel()
        else:
            messagebox.showerror("Error", msg, parent=self)

    def _cancel(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
#  LOGIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class LoginWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Webcam Security – Login")
        self.configure(bg=BG_DARK)
        self.geometry("380x300")
        self.resizable(False, False)
        self.authenticated = False

        tk.Label(self, text="🔒  Webcam Spyware Security",
                 font=("Segoe UI", 14, "bold"),
                 fg=FG_WHITE, bg=BG_DARK).pack(pady=(30, 4))

        tk.Label(self, text="Supraja Technologies",
                 font=("Segoe UI", 10),
                 fg=FG_GRAY, bg=BG_DARK).pack(pady=(0, 20))

        form = tk.Frame(self, bg=BG_DARK)
        form.pack()

        tk.Label(form, text="Username:", fg=FG_WHITE, bg=BG_DARK,
                 font=("Segoe UI", 10), width=10, anchor="e").grid(row=0, column=0, pady=6)
        self.user_var = tk.StringVar(value="admin")
        tk.Entry(form, textvariable=self.user_var,
                 font=("Segoe UI", 11), width=18
                 ).grid(row=0, column=1, pady=6, padx=6)

        tk.Label(form, text="Password:", fg=FG_WHITE, bg=BG_DARK,
                 font=("Segoe UI", 10), width=10, anchor="e").grid(row=1, column=0, pady=6)
        self.pass_var = tk.StringVar()
        tk.Entry(form, textvariable=self.pass_var,
                 show="*", font=("Segoe UI", 11), width=18
                 ).grid(row=1, column=1, pady=6, padx=6)

        self.bind("<Return>", lambda e: self._login())

        make_button(self, "Login", self._login,
                    BTN_BLUE, hov=BTN_BLUE_HOV, width=16,
                    font_size=11).pack(pady=20)

        self.err_label = tk.Label(self, text="", fg=FG_RED,
                                  bg=BG_DARK, font=("Segoe UI", 10))
        self.err_label.pack()

    def _login(self):
        user = verify_user(self.user_var.get().strip(),
                           self.pass_var.get())
        if user:
            CURRENT_USER["username"] = user["username"]
            CURRENT_USER["role"]     = user["role"]
            self.authenticated = True
            add_log("Login", f"User '{user['username']}' logged in",
                    user["username"])
            self.destroy()
        else:
            self.err_label.config(text="❌  Invalid username or password.")


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Init DB first
    init_db()

    # Show login window
    login = LoginWindow()
    login.mainloop()

    if not login.authenticated:
        sys.exit(0)

    # Launch main app
    app = WebcamSecurityApp()
    app.mainloop()
