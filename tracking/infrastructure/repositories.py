from tracking.infrastructure.models import TrackingRecord as TrackingRecordModel
from tracking.domain.entities import TrackingRecord

class TrackingRecordRepository:
    """Repository for managing persistence of tracking records."""

    @staticmethod
    def save(record: TrackingRecord) -> TrackingRecord:
        row = TrackingRecordModel.create(
            device_id=record.device_id,
            latitude=record.latitude,
            longitude=record.longitude,
            created_at=record.created_at
        )
        return TrackingRecord(
            row.device_id,
            row.latitude,
            row.longitude,
            row.created_at,
            row.id
        )
