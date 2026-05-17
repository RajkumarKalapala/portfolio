"""
gui/email_dialog.py
Generate OTP and send via SMTP alert email.
Also lets admin configure SMTP settings.
"""

import tkinter as tk
from tkinter import messagebox
import threading

from core.password_gen  import generate_otp, generate_password
from core.email_sender  import send_otp_email, send_alert_email

BG    = "#0a0a0a"
GREEN = "#00ff41"
GREY  = "#1a1a1a"
MONO  = ("Courier New", 10)


class EmailDialog(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("USBLOCKR – OTP & Email")
        self.geometry("520x540")
        self.configure(bg=BG)
        self._smtp = db.get_smtp()
        self._otp  = None
        self._build()

    def _build(self):
        tk.Label(self, text="🔑  OTP Generator & Email Alert",
                 font=("Courier New", 13, "bold"),
                 fg=GREEN, bg=BG).pack(pady=(16, 10))

        # ── SMTP config ───────────────────────────────────────────────────────
        smtp_frm = tk.LabelFrame(self, text=" SMTP Configuration ",
                                 font=MONO, fg=GREEN, bg=BG,
                                 bd=1, relief="solid")
        smtp_frm.pack(fill="x", padx=20, pady=(0, 10))

        fields = [
            ("SMTP Host",  "host",     "smtp.gmail.com"),
            ("SMTP Port",  "port",     "587"),
            ("Username",   "username", "your@gmail.com"),
            ("Password",   "password", ""),
            ("Alert To",   "alert_to", "admin@example.com"),
        ]
        self._smtp_entries = {}
        for i, (label, key, default) in enumerate(fields):
            tk.Label(smtp_frm, text=label + ":", font=MONO,
                     fg=GREEN, bg=BG, anchor="w", width=12
                     ).grid(row=i, column=0, sticky="w", padx=8, pady=3)
            show = "*" if key == "password" else ""
            e = tk.Entry(smtp_frm, font=MONO, bg=GREY, fg=GREEN,
                         insertbackground=GREEN, relief="flat",
                         bd=1, show=show,
                         highlightthickness=1, highlightcolor=GREEN,
                         highlightbackground="#333")
            e.insert(0, self._smtp.get(key, default))
            e.grid(row=i, column=1, sticky="ew", padx=8, pady=3, ipady=3)
            self._smtp_entries[key] = e
        smtp_frm.columnconfigure(1, weight=1)

        tk.Button(smtp_frm, text="Save SMTP Config",
                  font=MONO, fg=BG, bg=GREEN,
                  relief="flat", command=self._save_smtp
                  ).grid(row=len(fields), column=0, columnspan=2,
                         pady=6, ipadx=12, ipady=4)

        # ── OTP section ───────────────────────────────────────────────────────
        otp_frm = tk.LabelFrame(self, text=" Generate & Send OTP ",
                                font=MONO, fg=GREEN, bg=BG,
                                bd=1, relief="solid")
        otp_frm.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(otp_frm, text="To Email:", font=MONO,
                 fg=GREEN, bg=BG, anchor="w").grid(
            row=0, column=0, sticky="w", padx=8, pady=6)
        self.to_entry = tk.Entry(otp_frm, font=MONO, bg=GREY, fg=GREEN,
                                  insertbackground=GREEN, relief="flat",
                                  highlightthickness=1, highlightcolor=GREEN,
                                  highlightbackground="#333")
        self.to_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=6, ipady=3)
        otp_frm.columnconfigure(1, weight=1)

        self.otp_display = tk.Label(otp_frm, text="OTP: ------",
                                     font=("Courier New", 16, "bold"),
                                     fg=GREEN, bg=BG)
        self.otp_display.grid(row=1, column=0, columnspan=2, pady=6)

        btn_row = tk.Frame(otp_frm, bg=BG)
        btn_row.grid(row=2, column=0, columnspan=2, pady=(0, 8))
        tk.Button(btn_row, text="Generate OTP",
                  font=MONO, fg=BG, bg=GREEN,
                  relief="flat", command=self._gen_otp
                  ).pack(side="left", ipadx=10, ipady=4, padx=4)
        tk.Button(btn_row, text="Send via Email",
                  font=MONO, fg=BG, bg=GREEN,
                  relief="flat", command=self._send_otp
                  ).pack(side="left", ipadx=10, ipady=4, padx=4)

        self.status_lbl = tk.Label(self, text="", font=MONO,
                                    fg="#aaffaa", bg=BG)
        self.status_lbl.pack(pady=4)

        tk.Button(self, text="Close", font=MONO, fg=GREEN, bg=BG,
                  relief="solid", bd=1, command=self.destroy
                  ).pack(pady=6, ipadx=16, ipady=4)

    def _save_smtp(self):
        d = {k: e.get().strip() for k, e in self._smtp_entries.items()}
        self.db.save_smtp(d["host"], d["port"], d["username"],
                          d["password"], d["alert_to"])
        self._smtp = self.db.get_smtp()
        messagebox.showinfo("SMTP", "SMTP configuration saved!", parent=self)

    def _gen_otp(self):
        self._otp = generate_otp(6)
        self.otp_display.config(text=f"OTP:  {self._otp}")
        self.status_lbl.config(text="OTP generated. Click 'Send via Email'.")

    def _send_otp(self):
        if not self._otp:
            self._gen_otp()
        to   = self.to_entry.get().strip()
        smtp = self.db.get_smtp()
        if not to:
            messagebox.showwarning("Email", "Enter recipient email.", parent=self)
            return
        self.status_lbl.config(text="Sending …")
        self.update()

        def _run():
            ok, msg = send_otp_email(
                to_addr   = to,
                otp       = self._otp,
                smtp_user = smtp.get("username", ""),
                smtp_pass = smtp.get("password", ""),
            )
            self.after(0, lambda: self.status_lbl.config(
                text=("✔ " if ok else "✘ ") + msg
            ))
        threading.Thread(target=_run, daemon=True).start()
