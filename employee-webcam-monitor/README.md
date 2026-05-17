# Webcam Spyware Security System
**Supraja Technologies | Cyber Security Internship Project**

---

## Overview
A Python/Tkinter desktop application that provides physical security control
over a Windows webcam using the Windows Registry, with:
- Camera Enable / Disable via HKLM registry
- Privacy Schedules (auto-block at specified times)
- Face Recognition enrollment
- Activity Log viewer
- Admin / User role management
- Dark-themed professional GUI

---

## Project Structure
```
webcam_security/
├── main.py            ← Launch this file (GUI + all features)
├── database.py        ← SQLite: logs, schedules, users, faces
├── camera_control.py  ← Windows Registry webcam control
├── scheduler.py       ← Background privacy schedule thread
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Install Python (3.10+)
Download from https://python.org — make sure to check "Add Python to PATH".

### 2. Install dependencies
Open Command Prompt in the project folder:
```
pip install Pillow opencv-python
```

For face recognition (optional, harder to install):
```
pip install cmake dlib face-recognition
```
> If dlib fails, skip it. The app works without face recognition.

### 3. Run as Administrator (REQUIRED for camera control)
- Right-click `main.py` → "Run with Python" → OR
- Open CMD as Administrator:
  ```
  python main.py
  ```

---

## Default Login
| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | Admin@123 | Admin |

---

## Features Map (matches Project Enhancements)

| # | Enhancement                        | Where in App                          |
|---|------------------------------------|---------------------------------------|
| 1 | Beginner-friendly GUI              | main.py – dark tkinter UI             |
| 2 | Face Recognition                   | "Register Face" button → webcam popup |
| 3 | Group Policy (Admin/User roles)    | database.py users table               |
| 4 | Intruder Detection (snapshot)      | Face registration saves images        |
| 5 | Schedule Webcam Access             | Privacy Schedules section             |
| 6 | Activity Monitoring & Alert System | View Logs window                      |
| 7 | Auto Password Generation + SMTP    | database.py hash_password + smtplib   |

---

## How Camera Control Works
The app writes to:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\
CapabilityAccessManager\ConsentStore\webcam
```
- Value `Allow` → camera enabled system-wide
- Value `Deny`  → camera disabled system-wide

This requires **Administrator** privileges.

---

## Privacy Schedules
- Add schedules in HH:MM format (24-hour)
- The background thread checks every 60 seconds
- If current time is inside an active schedule, camera is auto-disabled
- Example: 22:00 → 06:00 blocks camera overnight

---

## Project Information
- **Project Name:** Web Cam Security from Spyware
- **Company:** Supraja Technologies
- **Duration:** 01-DEC-2025 to 31-DEC-2025
- **Status:** Completed
