"""
gui/login_window.py
Login dialog for USBLOCKR. Matches the dark theme.
"""

import tkinter as tk
from tkinter import messagebox

BG    = "#0a0a0a"
GREEN = "#00ff41"
GREY  = "#1a1a1a"
MONO  = ("Courier New", 11)


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, db, callback):
        super().__init__(parent)
        self.db       = db
        self.callback = callback

        self.title("USBLOCKR – Login")
        self.geometry("380x260")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: None)   # force login

        # centre on parent
        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width()  - 380) // 2
        py = parent.winfo_y() + (parent.winfo_height() - 260) // 2
        self.geometry(f"+{px}+{py}")

        self._build()

    def _build(self):
        tk.Label(self, text="🔐  USBLOCKR Login",
                 font=("Courier New", 14, "bold"),
                 fg=GREEN, bg=BG).pack(pady=(24, 16))

        frm = tk.Frame(self, bg=BG)
        frm.pack(padx=30, fill="x")

        tk.Label(frm, text="Username:", font=MONO, fg=GREEN, bg=BG,
                 anchor="w").grid(row=0, column=0, sticky="w", pady=4)
        self.user_entry = tk.Entry(frm, font=MONO, bg=GREY, fg=GREEN,
                                   insertbackground=GREEN, relief="flat",
                                   bd=1, highlightthickness=1,
                                   highlightcolor=GREEN,
                                   highlightbackground="#333")
        self.user_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0), ipady=4)

        tk.Label(frm, text="Password:", font=MONO, fg=GREEN, bg=BG,
                 anchor="w").grid(row=1, column=0, sticky="w", pady=4)
        self.pass_entry = tk.Entry(frm, font=MONO, bg=GREY, fg=GREEN,
                                   show="*", insertbackground=GREEN,
                                   relief="flat", bd=1,
                                   highlightthickness=1,
                                   highlightcolor=GREEN,
                                   highlightbackground="#333")
        self.pass_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), ipady=4)
        frm.columnconfigure(1, weight=1)

        tk.Button(self, text="  LOGIN  ",
                  font=("Courier New", 11, "bold"),
                  fg="black", bg=GREEN,
                  activeforeground="black", activebackground="#aaffaa",
                  relief="flat", cursor="hand2",
                  command=self._login).pack(pady=(20, 0), ipadx=20, ipady=6)

        self.user_entry.focus()
        self.pass_entry.bind("<Return>", lambda e: self._login())
        self.user_entry.bind("<Return>", lambda e: self.pass_entry.focus())

        # hint
        tk.Label(self, text="Default: admin / admin123  or  user1 / user123",
                 font=("Courier New", 8), fg="#444", bg=BG).pack(pady=(10, 0))

    def _login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get()
        if not u or not p:
            messagebox.showwarning("Login", "Enter username and password.",
                                   parent=self)
            return
        user = self.db.authenticate(u, p)
        if user:
            self.destroy()
            self.callback(user)
        else:
            messagebox.showerror("Login Failed",
                                 "Incorrect username or password.",
                                 parent=self)
            self.pass_entry.delete(0, "end")
