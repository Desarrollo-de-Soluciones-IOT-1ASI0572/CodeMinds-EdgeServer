from tracking.infrastructure.models import TrackingRecord as TrackingRecordModel
from tracking.domain.entities import TrackingRecord
from datetime import datetime

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
    
    @staticmethod
    def get_all() -> list[TrackingRecord]:
        locations = TrackingRecordModel.select()
        result = []
        for loc in locations:
            created_at = loc.created_at
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", ""))
            result.append(TrackingRecord(
                loc.device_id,
                loc.latitude,
                loc.longitude,
                created_at,
                loc.id
            ))
        return result
