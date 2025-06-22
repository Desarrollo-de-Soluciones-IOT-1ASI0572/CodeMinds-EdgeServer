from identity_assignment.domain.entities import Student, Wristband
from identity_assignment.infrastructure.models import StudentModel, WristbandModel

class StudentRepository:
    """Repository for managing student persistence."""

    @staticmethod
    def save(student: Student) -> Student:
        """Save a student entity to the database."""
        student_model = StudentModel.create(
            name=student.name,
            last_name=student.last_name,
            home_address=student.home_address,
            school_address=student.school_address,
            student_photo_url=student.student_photo_url,
            parent_profile_id=student.parent_profile_id,
            created_at=student.created_at
        )

        return Student(
            name=student_model.name,
            last_name=student_model.last_name,
            home_address=student_model.home_address,
            school_address=student_model.school_address,
            student_photo_url=student_model.student_photo_url,
            parent_profile_id=student_model.parent_profile_id,
            id=student_model.id,
            created_at=student_model.created_at
        )


class WristbandRepository:
    """Repository for managing wristband persistence."""

    @staticmethod
    def save(wristband: Wristband) -> Wristband:
        """Save a wristband entity to the database."""
        wristband_model = WristbandModel.create(
            rfid_code=wristband.rfid_code,
            wristband_status=wristband.wristband_status,
            student=wristband.student_id,
            created_at=wristband.created_at
        )

        return Wristband(
            rfid_code=wristband_model.rfid_code,
            wristband_status=wristband_model.wristband_status,
            student_id=wristband_model.student.id,
            id=wristband_model.id,
            created_at=wristband_model.created_at
        )

    @staticmethod
    def find_by_rfid_code(rfid_code: str) -> Wristband | None:
        """Find a wristband by its RFID code."""
        try:
            wristband_model = WristbandModel.get(WristbandModel.rfid_code == rfid_code)
            return Wristband(
                rfid_code=wristband_model.rfid_code,
                wristband_status=wristband_model.wristband_status,
                student_id=wristband_model.student.id,
                id=wristband_model.id,
                created_at=wristband_model.created_at
            )
        except WristbandModel.DoesNotExist:
            return None
