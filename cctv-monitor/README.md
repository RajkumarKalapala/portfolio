# CCTV Unified Monitoring Platform — IT Cell

A centralized web application to monitor SIM-based CCTV cameras deployed across a city.

---

## Features

| Module | Description |
|--------|-------------|
| **Live Dashboard** | Real-time online/offline/intermittent status with auto-refresh every 30s |
| **Camera Management** | Full table with filtering by status, zone, provider; click to view details |
| **Geo Map** | SVG-based city map with hover tooltips for each camera |
| **Ticket System** | Raise and update repair tickets with priority and team assignment |
| **Reports & Analytics** | Zone-wise charts, provider distribution, data usage, CSV export |
| **Role-based Login** | Admin / Operator / Viewer roles |

---

## Setup & Run (Step-by-Step)

### Prerequisites
- Python 3.9 or above
- pip (Python package manager)

---

### Step 1: Install Python (if not installed)
Download from https://www.python.org/downloads/
During installation on Windows — check ✅ "Add Python to PATH"

---

### Step 2: Open Terminal / Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux**: Open Terminal app

---

### Step 3: Navigate to the project folder
```bash
cd path/to/cctv-monitor
```
Example: `cd C:\Users\YourName\Downloads\cctv-monitor`

---

### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```
This installs Flask and Flask-SQLAlchemy.

---

### Step 5: Run the application
```bash
python run.py
```

---

### Step 6: Open in browser
Go to: **http://127.0.0.1:5000**

---

## Login Credentials (Demo)

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Full access |
| `operator` | `op123` | Operational access |
| `viewer` | `view123` | Read-only |

---

## Project Structure

```
cctv-monitor/
├── run.py                    ← Start the app here
├── requirements.txt
├── backend/
│   └── app.py                ← Flask app, database models, API routes
├── frontend/
│   └── templates/
│       ├── base.html         ← Layout with sidebar & topbar
│       ├── login.html
│       ├── dashboard.html
│       ├── cameras.html
│       ├── tickets.html
│       ├── map.html
│       └── reports.html
└── data/
    └── cctv.db               ← SQLite database (auto-created on first run)
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/summary` | GET | Dashboard KPI summary |
| `/api/cameras` | GET | All camera data |
| `/api/tickets` | GET | All tickets |
| `/api/tickets/create` | POST | Create new ticket |
| `/api/tickets/update` | POST | Update ticket status |
| `/api/zone_stats` | GET | Per-zone breakdown |
| `/api/simulate_refresh` | GET | Simulate live status changes |

---

## Extending This Project

- **Real SIM API**: Replace simulated data in `app.py` with actual SIM provider API calls (Airtel, Jio, BSNL APIs)
- **Real Camera Ping**: Add `subprocess.run(['ping', camera_ip])` logic in a background thread
- **Email Alerts**: Use `smtplib` to send alerts when cameras go offline > threshold
- **PostgreSQL**: Change `SQLALCHEMY_DATABASE_URI` to `postgresql://user:pass@host/db`
- **RFID Asset Tagging**: Add asset_tag field to Camera model and scan integration
- **Authentication**: Replace simple hash auth with Flask-Login + JWT for production

---

## Tech Stack
- **Backend**: Python + Flask + Flask-SQLAlchemy
- **Database**: SQLite (upgradeable to PostgreSQL)
- **Frontend**: HTML5 + CSS3 + Vanilla JS (no heavy frameworks needed)
- **Fonts**: Exo 2 + Share Tech Mono (Google Fonts)
- **Icons**: Font Awesome 6

---

*Developed as part of IT Cell Internship Project 24 — Unified CCTV Monitoring Platform*
