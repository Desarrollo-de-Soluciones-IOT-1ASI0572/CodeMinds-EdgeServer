from datetime import datetime

class Device:
    def __init__(self, device_id, api_key, registered_at=None):
        self.device_id = device_id
        self.api_key = api_key
        self.registered_at = registered_at or datetime.now()

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "api_key": self.api_key,
            "registered_at": str(self.registered_at)
        }
