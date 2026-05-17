"""
gui/whitelist_window.py
Manage USB device whitelist.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog

BG    = "#0a0a0a"
GREEN = "#00ff41"
GREY  = "#1a1a1a"
MONO  = ("Courier New", 10)


class WhitelistWindow(tk.Toplevel):
    def __init__(self, parent, whitelist_mgr):
        super().__init__(parent)
        self.wm = whitelist_mgr
        self.title("USBLOCKR – USB Whitelist")
        self.geometry("620x420")
        self.configure(bg=BG)
        self._build()
        self._refresh()

    def _build(self):
        tk.Label(self, text="🛡  USB Device Whitelist",
                 font=("Courier New", 13, "bold"),
                 fg=GREEN, bg=BG).pack(pady=(14, 8))

        # listbox
        frm = tk.Frame(self, bg=BG)
        frm.pack(fill="both", expand=True, padx=20)
        sb = tk.Scrollbar(frm)
        sb.pack(side="right", fill="y")
        self.lb = tk.Listbox(frm, font=MONO, bg=GREY, fg=GREEN,
                              selectbackground=GREEN, selectforeground=BG,
                              relief="flat", bd=0,
                              yscrollcommand=sb.set)
        self.lb.pack(fill="both", expand=True)
        sb.config(command=self.lb.yview)

        # buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=10)
        for text, cmd in [
            ("➕  Add Device",    self._add),
            ("🗑  Remove Selected", self._remove),
            ("🔄  Refresh",       self._refresh),
        ]:
            tk.Button(btn_row, text=text, font=MONO,
                      fg=BG, bg=GREEN, relief="flat",
                      command=cmd).pack(side="left", padx=6,
                                        ipadx=8, ipady=4)

    def _refresh(self):
        self.lb.delete(0, "end")
        for item in self.wm.get_all():
            self.lb.insert("end",
                f"  {item['device_id']:<40}  {item['label']:<20}  "
                f"Added: {item['added_at']}")

    def _add(self):
        dev_id = simpledialog.askstring(
            "Add Device", "Enter Device ID (e.g. \\\\.\\PHYSICALDRIVE1):",
            parent=self)
        if not dev_id:
            return
        label = simpledialog.askstring(
            "Label", "Enter a label for this device (optional):",
            parent=self) or ""
        ok = self.wm.add_device(dev_id.strip(), label.strip())
        if ok:
            self._refresh()
        else:
            messagebox.showwarning("Whitelist", "Device already whitelisted.",
                                   parent=self)

    def _remove(self):
        sel = self.lb.curselection()
        if not sel:
            return
        line = self.lb.get(sel[0]).strip()
        dev_id = line.split()[0]
        if messagebox.askyesno("Remove", f"Remove {dev_id}?", parent=self):
            self.wm.remove_device(dev_id)
            self._refresh()
