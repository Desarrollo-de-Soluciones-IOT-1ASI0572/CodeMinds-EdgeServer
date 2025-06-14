from datetime import datetime

class RFIDEvent:
    def __init__(self, rfid_code: str, timestamp: datetime = None):
        self.rfid_code = rfid_code
        self.timestamp = timestamp or datetime.utcnow()
