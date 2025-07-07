from datetime import datetime

class Student:
    """Represents a student entity in the Identity context."""

    def __init__(self, name: str, last_name: str, home_address: str, school_address: str,
                 student_photo_url: str, parent_profile_id: int, id: int = None, created_at: datetime = None):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.home_address = home_address
        self.school_address = school_address
        self.student_photo_url = student_photo_url
        self.parent_profile_id = parent_profile_id
        self.created_at = created_at or datetime.now()


class Wristband:
    """Represents a wristband entity in the Identity context."""

    def __init__(self, rfid_code: str, wristband_status: str, student_id: int, id: int = None):
        self.id = id
        self.rfid_code = rfid_code
        self.wristband_status = wristband_status
        self.student_id = student_id
