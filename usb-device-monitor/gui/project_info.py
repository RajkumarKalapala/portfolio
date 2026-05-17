"""
gui/project_info.py
Project Information window – matches Image 2 layout.
"""

import tkinter as tk
from tkinter import ttk

BG    = "#0a0a0a"
GREEN = "#00ff41"
MONO  = ("Courier New", 10)


class ProjectInfoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Project Information")
        self.geometry("620x540")
        self.configure(bg="white")
        self._build()

    def _build(self):
        tk.Label(self, text="Project Information",
                 font=("Arial", 18, "bold"),
                 bg="white").pack(anchor="w", padx=20, pady=(20, 4))

        desc = (
            "This project was developed by Rajkumar Kalapala as part of a "
            "Cyber Security Internship. This project is designed to "
            "Secure the Organizations in Real World from Cyber Frauds "
            "performed by Hackers."
        )
        tk.Label(self, text=desc, wraplength=580, justify="left",
                 font=("Arial", 10), bg="white").pack(anchor="w",
                                                       padx=20, pady=(0, 12))

        # ── project details table ─────────────────────────────────────────────
        self._table(self, [
            ("Project Name",        "USB Physical Security"),
            ("Project Description", "Implementing Physical Security Policy on\n"
                                    "USB Ports in Organization for Physical Security"),
            ("Project Start Date",  "01-DEC-2025"),
            ("Project End Date",    "31-DEC-2025"),
            ("Project Status",      "Completed"),
        ])

        tk.Label(self, text="Developer Details",
                 font=("Arial", 13, "bold"), bg="white").pack(
            anchor="w", padx=20, pady=(14, 4))

        self._table(self, [
            ("Name",        "Rajkumar Kalapala"),
            ("Employee ID", "ST#IS#0000"),
            ("Email",       "rajkumar@example.com"),
        ], cols=["Name", "Employee ID", "Email"])

        tk.Label(self, text="Company Details",
                 font=("Arial", 13, "bold"), bg="white").pack(
            anchor="w", padx=20, pady=(14, 4))

        self._table(self, [
            ("Name",    "Supraja Technologies"),
            ("Email",   "contact@suprajatechnologies.com"),
            ("Website", "www.suprajatechnologies.com"),
        ])

        tk.Button(self, text="Close", font=("Arial", 10),
                  command=self.destroy).pack(pady=12, ipadx=16, ipady=4)

    def _table(self, parent, rows, cols=None):
        frm = tk.Frame(parent, bg="#ddd", bd=1, relief="solid")
        frm.pack(fill="x", padx=20, pady=2)

        # header
        headers = cols or ["Project Details", "Value"]
        for ci, h in enumerate(headers):
            tk.Label(frm, text=h, font=("Arial", 10, "bold"),
                     bg="#e8e8e8", relief="ridge", bd=1,
                     padx=8, pady=4, anchor="w"
                     ).grid(row=0, column=ci, sticky="nsew")

        for ri, (k, v) in enumerate(rows, start=1):
            tk.Label(frm, text=k, font=("Arial", 10),
                     bg="white", relief="ridge", bd=1,
                     padx=8, pady=4, anchor="nw"
                     ).grid(row=ri, column=0, sticky="nsew")
            tk.Label(frm, text=v, font=("Arial", 10),
                     bg="white", relief="ridge", bd=1,
                     padx=8, pady=4, anchor="nw", justify="left"
                     ).grid(row=ri, column=1, sticky="nsew", columnspan=max(1, len(headers)-1))

        frm.columnconfigure(1, weight=1)
