from flask import Blueprint, request, jsonify
from tracking.application.services import TrackingRecordApplicationService

tracking_api = Blueprint("tracking_api", __name__)
tracking_service = TrackingRecordApplicationService()

@tracking_api.route("/api/v1/tracking", methods=["POST"])
def create_tracking():
    """
    Create a new tracking record.
    Expected JSON: { "device_id": "...", "latitude": ..., "longitude": ..., "created_at": optional }
    """
    try:
        data = request.json
        device_id = data["device_id"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        created_at = data.get("created_at")

        record = tracking_service.create_tracking_record(
            device_id=device_id,
            latitude=latitude,
            longitude=longitude,
            created_at=created_at
        )

        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@tracking_api.route('/api/v1/tracking', methods=['GET'])
def get_locations():
    locations = tracking_service.get_all_locations()
    return jsonify([
        {
            'id': loc.id,
            'device_id': loc.device_id,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'created_at': loc.created_at.isoformat() + "Z" if loc.created_at else None
        }
        for loc in locations
    ])