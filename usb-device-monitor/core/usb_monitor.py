"""
core/usb_monitor.py
Monitor USB device insertion events on Windows using WMI.
Calls on_new_device(device_id) callback when a new USB drive appears.
"""

import threading
import time


class USBMonitor:
    def __init__(self, on_new_device=None):
        self.on_new_device = on_new_device
        self._running      = False
        self._thread       = None
        self._known        = set()

    def start(self):
        self._running = True
        self._thread  = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    # ── internal ──────────────────────────────────────────────────────────────
    def _get_usb_devices(self) -> set:
        """Return set of currently connected USB device IDs."""
        try:
            import wmi
            c = wmi.WMI()
            return {
                d.DeviceID
                for d in c.Win32_DiskDrive()
                if "USB" in (d.InterfaceType or "").upper()
            }
        except Exception:
            # wmi not available – fallback via subprocess
            try:
                import subprocess
                out = subprocess.check_output(
                    ["wmic", "diskdrive", "where",
                     "InterfaceType='USB'", "get", "DeviceID"],
                    stderr=subprocess.DEVNULL, text=True
                )
                lines = [l.strip() for l in out.splitlines()
                         if l.strip() and l.strip() != "DeviceID"]
                return set(lines)
            except Exception:
                return set()

    def _run(self):
        # seed known devices on start so we don't false-alarm existing ones
        self._known = self._get_usb_devices()

        while self._running:
            time.sleep(3)
            current = self._get_usb_devices()
            new_devs = current - self._known
            for dev in new_devs:
                if self.on_new_device:
                    self.on_new_device(dev)
            self._known = current
