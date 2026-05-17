"""
core/whitelist.py
USB Device Whitelisting – only devices in the whitelist are allowed.
"""


class WhitelistManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def is_allowed(self, device_id: str) -> bool:
        """Return True if device_id is on the whitelist."""
        allowed = self.db.get_whitelist()
        return device_id in allowed

    def add_device(self, device_id: str, label: str = "") -> bool:
        return self.db.add_to_whitelist(device_id, label)

    def remove_device(self, device_id: str) -> bool:
        return self.db.remove_from_whitelist(device_id)

    def get_all(self) -> list:
        return self.db.get_whitelist_full()
