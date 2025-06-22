from datetime import datetime
from .entities import Student, Wristband
from ..infrastructure.api.sensor_scan_api import SensorScanAPI
from ..infrastructure.repositories import StudentRepository, WristbandRepository

class IdentityAssignmentService:
    """Service for managing student identity assignments and wristbands."""

    def __init__(self, student_repository: StudentRepository, wristband_repository: WristbandRepository, sensor_scan_api: SensorScanAPI):
        """Initialize the IdentityAssignmentService."""
        self.student_repository = student_repository
        self.wristband_repository = wristband_repository
        self.sensor_scan_api = sensor_scan_api  # API para enviar escaneos

    def create_student(self, name: str, last_name: str, home_address: str, school_address: str,
                       student_photo_url: str, parent_profile_id: int) -> Student:
        """Create a new student and assign them a wristband."""
        student = Student(
            name=name,
            last_name=last_name,
            home_address=home_address,
            school_address=school_address,
            student_photo_url=student_photo_url,
            parent_profile_id=parent_profile_id
        )

        self.student_repository.save(student)

        # Asociar wristband
        wristband = self.create_wristband(student.id)

        return student

    def create_wristband(self, student_id: int) -> Wristband:
        """Create a new wristband for a student."""
        rfid_code = self.generate_rfid_code()

        wristband = Wristband(
            rfid_code=rfid_code,
            wristband_status="ACTIVE",
            student_id=student_id
        )

        self.wristband_repository.save(wristband)

        return wristband

    def generate_rfid_code(self) -> str:
        """Generate a unique RFID code."""
        return "RFID" + str(datetime.now().timestamp())

    def process_rfid_scan(self, rfid_code: str, scan_type: str) -> bool:
        """Handle a scanned RFID code and send it to the backend if valid.

        Args:
            rfid_code (str): The RFID code read from the device.
            scan_type (str): The type of scan, e.g., 'ENTRY' or 'EXIT'.

        Returns:
            bool: True if scan was successfully registered, False otherwise.
        """
        wristband = self.wristband_repository.find_by_rfid_code(rfid_code)

        if wristband and wristband.wristband_status == "ACTIVE":
            return self.sensor_scan_api.send_scan(scan_type=scan_type, wristband_id=wristband.id)

        return False
