from datetime import datetime

class Student:
    """Represents a student entity in the Identity context.

    Attributes:
        id (int, optional): Unique identifier for the student.
        name (str): Name of the student.
        last_name (str): Last name of the student.
        home_address (str): Student's home address.
        school_address (str): Student's school address.
        student_photo_url (str): URL of the student's photo.
        parent_profile_id (int): The parent's profile ID.
        created_at (datetime): Timestamp when the student record was created.
    """

    def __init__(self, name: str, last_name: str, home_address: str, school_address: str,
                 student_photo_url: str, parent_profile_id: int, id: int = None, created_at: datetime = None):
        """Initialize a Student instance.

        Args:
            name (str): Name of the student.
            last_name (str): Last name of the student.
            home_address (str): Home address of the student.
            school_address (str): School address of the student.
            student_photo_url (str): URL of the student's photo.
            parent_profile_id (int): The parent's profile ID.
            id (int, optional): Student identifier. Defaults to None.
            created_at (datetime, optional): Timestamp when the student was created. Defaults to None.
        """
        self.id = id
        self.name = name
        self.last_name = last_name
        self.home_address = home_address
        self.school_address = school_address
        self.student_photo_url = student_photo_url
        self.parent_profile_id = parent_profile_id
        self.created_at = created_at or datetime.now()  # Default to current time if not provided


class Wristband:
    """Represents a wristband entity in the Identity context.

    Attributes:
        id (int, optional): Unique identifier for the wristband.
        rfid_code (str): The RFID code associated with the wristband.
        wristband_status (str): The status of the wristband (e.g., ACTIVE, INACTIVE).
        student_id (int): The ID of the student associated with this wristband.
    """

    def __init__(self, rfid_code: str, wristband_status: str, student_id: int, id: int = None):
        """Initialize a Wristband instance.

        Args:
            rfid_code (str): RFID code of the wristband.
            wristband_status (str): Status of the wristband.
            student_id (int): The student ID to whom the wristband is assigned.
            id (int, optional): Wristband identifier. Defaults to None.
        """
        self.id = id
        self.rfid_code = rfid_code
        self.wristband_status = wristband_status
        self.student_id = student_id
