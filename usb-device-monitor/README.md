# USBLOCKR – USB Physical Security Tool
### Supraja Technologies | Cyber Security Internship

---

## WHAT THIS PROJECT DOES

USBLOCKR is a Windows desktop security application that:
1. **Disables / Enables USB ports** via Windows Registry (requires Admin)
2. **Identifies Intruders** – takes a webcam snapshot when an unknown USB is inserted
3. **USB Activity Monitoring** – background thread watches for new USB devices every 3 seconds
4. **USB Device Whitelisting** – only approved devices are allowed; others trigger an alert
5. **Automatic Password / OTP Generation** – creates secure OTPs and emails them via SMTP
6. **User Role System** – Admin and User roles stored in SQLite database
7. **Email Alerts** – sends intrusion alerts with snapshot attachment via Gmail/SMTP
8. **Activity Logs** – every action is recorded and viewable inside the app

---

## SETUP GUIDE (Windows 11)

### Step 1 – Install Python
Download Python 3.10 or newer from https://python.org
✅ During install: CHECK "Add Python to PATH"

### Step 2 – Install dependencies
Open Command Prompt in the USBLOCKR folder:

```
pip install opencv-python Pillow pywin32 wmi
```

> If `wmi` fails, run:  `pip install WMI`

### Step 3 – Run the project (as Administrator)

**Option A – Double click:**
```
run_as_admin.bat
```

**Option B – Manual (in an Administrator CMD):**
```
cd C:\path\to\USBLOCKR
python main.py
```

---

## DEFAULT LOGIN CREDENTIALS

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | Admin |
| user1    | user123   | User  |

> Change passwords after first login via User Management.

---

## GMAIL SMTP SETUP (for OTP emails)

1. Enable **2-Step Verification** on your Google account
2. Go to: Google Account → Security → App Passwords
3. Create an App Password for "Mail"
4. Use that 16-character password in the SMTP config inside USBLOCKR

---

## PROJECT STRUCTURE

```
USBLOCKR/
├── main.py                  ← Entry point (run this)
├── run_as_admin.bat         ← Double-click launcher
├── requirements.txt
│
├── core/
│   ├── usb_controller.py    ← Disable/Enable USB via Registry
│   ├── snapshot.py          ← Webcam intruder snapshot
│   ├── password_gen.py      ← OTP / password generation
│   ├── email_sender.py      ← SMTP email alerts
│   ├── usb_monitor.py       ← Background USB device watcher
│   └── whitelist.py         ← Whitelist manager
│
├── database/
│   └── db_manager.py        ← SQLite: users, logs, whitelist, SMTP config
│
├── gui/
│   ├── login_window.py      ← Login dialog
│   ├── log_viewer.py        ← Activity log viewer
│   ├── project_info.py      ← Project Information window
│   ├── email_dialog.py      ← OTP generator + SMTP config
│   ├── whitelist_window.py  ← USB whitelist manager
│   └── user_mgmt.py         ← Admin: add/delete users
│
├── snapshots/               ← Auto-created; stores intruder photos
└── logs/                    ← Activity logs
```

---

## NOTES

- **USB Disable/Enable** requires Administrator rights (Windows Registry: USBSTOR key)
- **Webcam** must be connected for snapshot feature
- All data is stored locally in `database/usblockr.db` (SQLite)
- No internet required except for SMTP email sending

---

*USBLOCKR – USB Physical Security | Supraja Technologies*
