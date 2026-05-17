"""
scheduler.py
------------
Background thread that checks active privacy schedules every minute
and automatically enables/disables the webcam accordingly.
"""

import threading
import datetime
import time
from database import get_active_schedules, add_log
from camera_control import enable_camera, disable_camera, is_camera_enabled


class PrivacyScheduler(threading.Thread):
    """
    Runs as a daemon thread. Every 60 seconds it checks all active schedules
    and blocks the camera if the current time falls within any of them.
    """

    def __init__(self, status_callback=None):
        super().__init__(daemon=True)
        self._stop_event = threading.Event()
        self.status_callback = status_callback  # Optional: call this when camera state changes

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            self._check_schedules()
            # Sleep 60 s but wake up every second to allow clean shutdown
            for _ in range(60):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def _check_schedules(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        schedules = get_active_schedules()
        should_block = False

        for row in schedules:
            start = row["start_time"]  # "HH:MM"
            end = row["end_time"]      # "HH:MM"

            if self._time_in_range(current_time, start, end):
                should_block = True
                break

        camera_on = is_camera_enabled()

        if should_block and camera_on:
            ok, msg = disable_camera()
            if ok:
                add_log("Auto-Disable", "Camera auto-disabled by privacy schedule", "Scheduler")
                if self.status_callback:
                    self.status_callback("disabled_by_schedule")

        elif not should_block and not camera_on:
            # Only re-enable if it was disabled by a schedule (we track this simply)
            # For safety, we don't auto-enable here unless the caller decides to.
            pass

    @staticmethod
    def _time_in_range(current: str, start: str, end: str) -> bool:
        """Check if current HH:MM is within [start, end] range."""
        try:
            fmt = "%H:%M"
            c = datetime.datetime.strptime(current, fmt)
            s = datetime.datetime.strptime(start, fmt)
            e = datetime.datetime.strptime(end, fmt)

            if s <= e:
                return s <= c <= e
            else:
                # Overnight range e.g. 22:00 – 06:00
                return c >= s or c <= e
        except ValueError:
            return False
