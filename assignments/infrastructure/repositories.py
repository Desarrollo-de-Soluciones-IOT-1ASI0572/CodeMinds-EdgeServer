from datetime import datetime
from assignments.domain.entities import Student, Wristband
from assignments.infrastructure.models import StudentModel, WristbandModel, ScanStateModel

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
        
class ScanStateRepository:
    """Repository for managing scan states."""
    
    def get_scan_count_by_wristband_id(self, wristband_id: int) -> int:
        """Get scan count by wristband ID."""
        try:
            state_model = ScanStateModel.select().where(
                ScanStateModel.wristband_id == wristband_id
            ).get()
            return state_model.scan_count
        except ScanStateModel.DoesNotExist:
            return 0  # No scans yet
    
    def increment_scan_count(self, wristband_id: int) -> int:
        """Increment scan count for wristband and return new count."""
        try:
            # Try to update existing record
            existing = ScanStateModel.select().where(
                ScanStateModel.wristband_id == wristband_id
            ).first()
            
            if existing:
                new_count = existing.scan_count + 1
                ScanStateModel.update(
                    scan_count=new_count,
                    last_scan_timestamp=datetime.now()
                ).where(
                    ScanStateModel.wristband_id == wristband_id
                ).execute()
                return new_count
            else:
                # Create new record with count = 1
                state_model = ScanStateModel.create(
                    wristband_id=wristband_id,
                    scan_count=1,
                    last_scan_timestamp=datetime.now()
                )
                return 1
                
        except Exception as e:
            print(f"[ERROR] Failed to increment scan count: {e}")
            raise

    def get_all_scan_states(self):
        """Get all scan states for debugging."""
        try:
            states = ScanStateModel.select()
            for state in states:
                print(f"[DEBUG] Wristband {state.wristband_id}: {state.scan_count} scans")
            return states
        except Exception as e:
            print(f"[ERROR] Failed to get scan states: {e}")
            return []
