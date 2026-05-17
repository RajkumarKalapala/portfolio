"""
core/usb_controller.py
Enable / Disable USB storage ports via Windows Registry.
Requires Administrator privileges.
"""

import sys

# HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR  →  Start
#   3 = enabled (manual)   |   4 = disabled
USBSTOR_KEY  = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
START_VALUE  = "Start"
ENABLED_VAL  = 3
DISABLED_VAL = 4

LOG_PATH = "logs/usb_actions.log"


def _write_registry(value: int):
    """Write Start value to USBSTOR key. Returns (ok, message)."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            USBSTOR_KEY,
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
        )
        winreg.SetValueEx(key, START_VALUE, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
        return True, "OK"
    except PermissionError:
        return False, (
            "Permission denied.\n"
            "Please run USBLOCKR as Administrator\n"
            "(Right-click → Run as administrator)."
        )
    except Exception as e:
        return False, str(e)


def disable_usb():
    """Disable USB storage ports. Returns (ok, message)."""
    return _write_registry(DISABLED_VAL)


def enable_usb():
    """Enable USB storage ports. Returns (ok, message)."""
    return _write_registry(ENABLED_VAL)


def get_usb_status() -> bool:
    """Return True if USB storage is currently enabled."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            USBSTOR_KEY,
            0,
            winreg.KEY_READ | winreg.KEY_WOW64_64KEY
        )
        val, _ = winreg.QueryValueEx(key, START_VALUE)
        winreg.CloseKey(key)
        return val == ENABLED_VAL
    except Exception:
        return True   # assume enabled if can't read
