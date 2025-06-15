from tracking.domain.entities import TrackingRecord
from tracking.domain.services import TrackingRecordService
from tracking.infrastructure.repositories import TrackingRecordRepository

class TrackingRecordApplicationService:
    """Application service for vehicle tracking records."""

    def __init__(self):
        self.tracking_repository = TrackingRecordRepository()
        self.tracking_service = TrackingRecordService()

    def create_tracking_record(self, device_id: str, latitude: float, longitude: float, created_at: str) -> TrackingRecord:
        """Create and persist a tracking record."""
        record = self.tracking_service.create_record(device_id, latitude, longitude, created_at)
        return self.tracking_repository.save(record)
