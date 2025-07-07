from flask import Blueprint, request, jsonify
from assignments.application.services import ScanProcessingService

scan_api = Blueprint("scan_api", __name__)
scan_service = ScanProcessingService(token="eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJwYXJlbnQiLCJpYXQiOjE3NTE4Nzc4MjksImV4cCI6MTc1MjQ4MjYyOX0.y9CDqBQYTh36AO_-U2EU-Lk_qDzY72QLC-fpfIagvgwbPPms8TkRc8H-6rs4cPX-")  # Initialize with no token for simplicity

@scan_api.route("/api/v1/sensor-scans", methods=["POST"])
def process_scan():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    try:
        device_id = data["device_id"]
        rfid_code = data["rfid_code"]
        scan_type = data["scanType"]

        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"error": "API key is required"}), 401

        success = scan_service.process_scan(device_id, rfid_code, scan_type, api_key)

        if success:
            return jsonify({"message": "Scan registered successfully"}), 200
        else:
            return jsonify({"error": "Scan failed"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
