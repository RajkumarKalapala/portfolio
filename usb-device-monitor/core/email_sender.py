"""
core/email_sender.py
Send alert emails via SMTP (Gmail / any SMTP server).
Configure SMTP settings in config.py or pass them directly.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime

# ── Default SMTP config (override via config.py or DB settings) ───────────────
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = ""     # set in config or EmailDialog
SMTP_PASS     = ""     # set in config or EmailDialog
ALERT_TO      = ""     # admin email to receive alerts


def send_alert_email(device_id: str, snapshot_path: str = None,
                     smtp_user: str = None, smtp_pass: str = None,
                     to_addr: str = None) -> tuple:
    """
    Send a USB intrusion alert email with optional snapshot attachment.
    Returns (ok: bool, message: str).
    """
    _user = smtp_user or SMTP_USER
    _pass = smtp_pass or SMTP_PASS
    _to   = to_addr   or ALERT_TO

    if not _user or not _pass or not _to:
        return False, "SMTP credentials not configured."

    now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subj = f"⚠ USBLOCKR ALERT – Unauthorised USB Detected [{now}]"
    body = (
        f"<h2 style='color:red'>USBLOCKR Security Alert</h2>"
        f"<p><b>Timestamp:</b> {now}</p>"
        f"<p><b>Device ID:</b> {device_id}</p>"
        f"<p>An unauthorised USB device was inserted into a protected system.</p>"
        f"<p>Please review the attached snapshot and take appropriate action.</p>"
        f"<hr><small>USBLOCKR – USB Physical Security | Supraja Technologies</small>"
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subj
    msg["From"]    = _user
    msg["To"]      = _to
    msg.attach(MIMEText(body, "html"))

    # attach snapshot if available
    if snapshot_path and os.path.exists(snapshot_path):
        with open(snapshot_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        fname = os.path.basename(snapshot_path)
        part.add_header("Content-Disposition", f'attachment; filename="{fname}"')
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
            s.ehlo()
            s.starttls()
            s.login(_user, _pass)
            s.sendmail(_user, _to, msg.as_string())
        return True, "Alert email sent."
    except Exception as e:
        return False, str(e)


def send_otp_email(to_addr: str, otp: str,
                   smtp_user: str = None, smtp_pass: str = None) -> tuple:
    """Send an OTP to the given address for authentication."""
    _user = smtp_user or SMTP_USER
    _pass = smtp_pass or SMTP_PASS

    if not _user or not _pass:
        return False, "SMTP credentials not configured."

    subj = "USBLOCKR – Your One-Time Password"
    body = (
        f"<h2>USBLOCKR Authentication</h2>"
        f"<p>Your One-Time Password is:</p>"
        f"<h1 style='letter-spacing:8px;color:#006400'>{otp}</h1>"
        f"<p>This OTP is valid for one login attempt only.</p>"
        f"<small>USBLOCKR – USB Physical Security</small>"
    )
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subj
    msg["From"]    = _user
    msg["To"]      = to_addr
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
            s.ehlo()
            s.starttls()
            s.login(_user, _pass)
            s.sendmail(_user, to_addr, msg.as_string())
        return True, "OTP sent."
    except Exception as e:
        return False, str(e)
