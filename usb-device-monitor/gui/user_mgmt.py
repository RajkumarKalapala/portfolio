"""
gui/user_mgmt.py
Admin-only: add/delete users, assign roles.
"""

import tkinter as tk
from tkinter import messagebox, ttk

BG    = "#0a0a0a"
GREEN = "#00ff41"
GREY  = "#1a1a1a"
MONO  = ("Courier New", 10)


class UserMgmtWindow(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("USBLOCKR – User Management")
        self.geometry("660x460")
        self.configure(bg=BG)
        self._build()
        self._refresh()

    def _build(self):
        tk.Label(self, text="👤  User Management",
                 font=("Courier New", 13, "bold"),
                 fg=GREEN, bg=BG).pack(pady=(14, 8))

        # user table
        cols = ("ID", "Username", "Role", "Email")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140 if c != "ID" else 50)
        style = ttk.Style()
        style.configure("Treeview",
                        background=GREY, foreground=GREEN,
                        fieldbackground=GREY, font=MONO)
        style.configure("Treeview.Heading", background="#111", foreground=GREEN)
        self.tree.pack(fill="both", expand=True, padx=20)

        # add user form
        form = tk.LabelFrame(self, text=" Add New User ", font=MONO,
                              fg=GREEN, bg=BG, bd=1, relief="solid")
        form.pack(fill="x", padx=20, pady=8)

        labels = ["Username", "Password", "Role", "Email"]
        self._entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(form, text=lbl + ":", font=MONO, fg=GREEN,
                     bg=BG, width=10, anchor="w"
                     ).grid(row=0, column=i*2, padx=4, pady=6, sticky="w")
            if lbl == "Role":
                var = tk.StringVar(value="user")
                w = tk.OptionMenu(form, var, "user", "admin")
                w.configure(font=MONO, bg=GREY, fg=GREEN,
                            activebackground=GREEN, highlightthickness=0)
                w["menu"].configure(bg=GREY, fg=GREEN)
                w.grid(row=0, column=i*2+1, padx=4, pady=6, sticky="ew")
                self._entries[lbl] = var
            else:
                show = "*" if lbl == "Password" else ""
                e = tk.Entry(form, font=MONO, bg=GREY, fg=GREEN,
                             insertbackground=GREEN, relief="flat",
                             highlightthickness=1, highlightcolor=GREEN,
                             highlightbackground="#333", show=show, width=14)
                e.grid(row=0, column=i*2+1, padx=4, pady=6, ipady=3)
                self._entries[lbl] = e

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=6)
        for text, cmd in [
            ("➕  Add User",     self._add_user),
            ("🗑  Delete User",  self._del_user),
            ("🔄  Refresh",     self._refresh),
        ]:
            tk.Button(btn_row, text=text, font=MONO, fg=BG, bg=GREEN,
                      relief="flat", command=cmd
                      ).pack(side="left", padx=6, ipadx=8, ipady=4)

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for u in self.db.list_users():
            self.tree.insert("", "end", values=(
                u["id"], u["username"], u["role"], u["email"]))

    def _add_user(self):
        uname = self._entries["Username"].get().strip()
        pw    = self._entries["Password"].get()
        role  = self._entries["Role"].get()
        email = self._entries["Email"].get().strip()
        if not uname or not pw:
            messagebox.showwarning("Add User", "Username and password required.",
                                   parent=self)
            return
        ok, msg = self.db.add_user(uname, pw, role, email)
        if ok:
            self._refresh()
            for key in ["Username", "Password", "Email"]:
                e = self._entries[key]
                if isinstance(e, tk.Entry):
                    e.delete(0, "end")
        else:
            messagebox.showerror("Add User", msg, parent=self)

    def _del_user(self):
        sel = self.tree.selection()
        if not sel:
            return
        vals    = self.tree.item(sel[0], "values")
        uname   = vals[1]
        if uname == "admin":
            messagebox.showwarning("Delete", "Cannot delete the admin user.",
                                   parent=self)
            return
        if messagebox.askyesno("Delete", f"Delete user '{uname}'?", parent=self):
            self.db.delete_user(uname)
            self._refresh()
