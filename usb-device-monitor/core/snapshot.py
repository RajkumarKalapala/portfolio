"""
core/snapshot.py
Capture a snapshot using the system webcam to identify intruders.
Saved to snapshots/ folder with timestamp filename.
"""

import os
import datetime

SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "snapshots")


def take_snapshot() -> tuple:
    """
    Capture a frame from the default webcam.
    Returns (filepath, None) on success or (None, error_message) on failure.
    """
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SNAPSHOT_DIR, f"intruder_{ts}.jpg")

    try:
        import cv2
    except ImportError:
        return None, "opencv-python not installed. Run: pip install opencv-python"

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None, "No webcam found. Connect a camera and try again."

    # warm-up frames for exposure adjustment
    for _ in range(5):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        return None, "Failed to capture frame from webcam."

    cv2.imwrite(path, frame)
    return path, None
