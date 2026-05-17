"""
gui/log_viewer.py
View activity logs in a scrollable dark-themed window.
"""

import tkinter as tk

BG    = "#0a0a0a"
GREEN = "#00ff41"
GREY  = "#111"
MONO  = ("Courier New", 10)


class LogViewer(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = parent.db
        self.title("USBLOCKR – Activity Logs")
        self.geometry("720x480")
        self.configure(bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="📋  Activity Logs",
                 font=("Courier New", 13, "bold"),
                 fg=GREEN, bg=BG).pack(pady=(12, 6))

        txt = tk.Text(self, font=MONO, bg=GREY, fg=GREEN,
                      insertbackground=GREEN, relief="flat",
                      state="normal", wrap="none")
        sb_y = tk.Scrollbar(self, orient="vertical",   command=txt.yview)
        sb_x = tk.Scrollbar(self, orient="horizontal", command=txt.xview)
        txt.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        sb_y.pack(side="right",  fill="y")
        sb_x.pack(side="bottom", fill="x")
        txt.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        logs = self.db.get_logs()
        header = f"{'Timestamp':<22} {'User':<15} {'Action'}\n"
        header += "-" * 70 + "\n"
        txt.insert("end", header)
        for row in logs:
            line = (f"{row['timestamp']:<22} "
                    f"{row['username']:<15} "
                    f"{row['action']}\n")
            txt.insert("end", line)
        txt.configure(state="disabled")

        tk.Button(self, text="Close", font=MONO, fg=BG, bg=GREEN,
                  relief="flat", command=self.destroy
                  ).pack(pady=6, ipadx=16, ipady=4)
