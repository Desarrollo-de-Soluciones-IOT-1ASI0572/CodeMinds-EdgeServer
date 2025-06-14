from datetime import datetime

class Device:
    def __init__(self, rfid_code, api_key, student_name=None, registered_at=None):
        self.rfid_code = rfid_code
        self.api_key = api_key
        self.student_name = student_name
        self.registered_at = registered_at or datetime.now()

    def to_dict(self):
        return {
            "rfid_code": self.rfid_code,
            "api_key": self.api_key,
            "student_name": self.student_name,
            "registered_at": str(self.registered_at)
        }
