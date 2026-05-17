"""
camera_control.py
-----------------
Controls webcam access via Windows Registry.
Registry Path: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\
               CurrentVersion\CapabilityAccessManager\ConsentStore\webcam
Value "Allow" → Enabled | Value "Deny" → Disabled
Requires Administrator privileges to write to HKLM.
"""

import sys
import os
import subprocess

WINDOWS = sys.platform == "win32"

REGISTRY_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"

def is_admin():
    """Check if the script is running with admin privileges."""
    if not WINDOWS:
        return False
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def request_admin():
    """Re-launch the script with admin privileges."""
    if not WINDOWS:
        return
    import ctypes
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

def get_camera_status():
    """
    Returns 'Allow' if camera is enabled, 'Deny' if disabled,
    or 'Unknown' if status can't be read.
    """
    if not WINDOWS:
        return "Unknown (Non-Windows)"
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            REGISTRY_PATH,
            0,
            winreg.KEY_READ
        )
        value, _ = winreg.QueryValueEx(key, "Value")
        winreg.CloseKey(key)
        return value  # "Allow" or "Deny"
    except FileNotFoundError:
        return "Allow"  # Default: allowed if key doesn't exist
    except PermissionError:
        return "Unknown (Need Admin)"
    except Exception as e:
        return f"Unknown ({e})"

def set_camera_status(status: str) -> tuple[bool, str]:
    """
    Set camera status.
    status: "Allow" or "Deny"
    Returns (success: bool, message: str)
    """
    if not WINDOWS:
        return False, "Registry control only available on Windows."
    
    if status not in ("Allow", "Deny"):
        return False, f"Invalid status: {status}. Use 'Allow' or 'Deny'."
    
    if not is_admin():
        return False, "Administrator privileges required to modify registry."
    
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            REGISTRY_PATH,
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "Value", 0, winreg.REG_SZ, status)
        winreg.CloseKey(key)
        return True, f"Camera {status}d successfully."
    except PermissionError:
        return False, "Permission denied. Run the application as Administrator."
    except Exception as e:
        return False, f"Registry error: {e}"

# def enable_camera() -> tuple[bool, str]:
#     """Enable the webcam system-wide."""
#     return set_camera_status("Allow")

# def disable_camera() -> tuple[bool, str]:
#     """Disable the webcam system-wide."""
#     return set_camera_status("Deny")

def enable_camera() -> tuple[bool, str]:
    """Enable webcam device."""
    try:
        subprocess.run(
            'powershell "Get-PnpDevice -Class Camera | Enable-PnpDevice -Confirm:$false"',
            shell=True,
            check=True
        )
        return True, "Camera enabled successfully."
    except Exception as e:
        return False, f"Error enabling camera: {e}"

def disable_camera() -> tuple[bool, str]:
    """Disable webcam device."""
    try:
        subprocess.run(
            'powershell "Get-PnpDevice -Class Camera | Disable-PnpDevice -Confirm:$false"',
            shell=True,
            check=True
        )
        return True, "Camera disabled successfully."
    except Exception as e:
        return False, f"Error disabling camera: {e}"

# def is_camera_enabled() -> bool:
#     """Returns True if camera is currently allowed."""
#     status = get_camera_status()
#     return status.lower() == "allow"
# def is_camera_enabled() -> bool:
#     """Check whether camera device is enabled."""
#     try:
#         result = subprocess.check_output(
#             [
#                 "powershell",
#                 "-Command",
#                 "(Get-PnpDevice -Class Camera).Status"
#             ],
#             text=True
#         ).strip()

#         # return result == "OK"
#         return "OK" in result.upper()

#     except Exception as e:
#         print("Status check error:", e)
#         return False
    
def is_camera_enabled() -> bool:
    """Check whether camera device is enabled."""
    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-PnpDevice -Class Camera).Status"
            ],
            text=True
        ).strip()

        print("Camera Status:", result)

        return "OK" in result.upper()

    except Exception as e:
        print("Status check error:", e)
        return False
