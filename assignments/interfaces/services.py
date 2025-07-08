from flask import Blueprint, request, jsonify
from assignments.application.services import ScanProcessingService

scan_api = Blueprint("scan_api", __name__)
scan_service = ScanProcessingService(token="eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJwYXJlbnQiLCJpYXQiOjE3NTE5NDEyMTgsImV4cCI6MTc1MjU0NjAxOH0.Bm6Ej3IYgC10U5JWsY7nWhSE2NfE-RJliFGT48QaO4fiVuUyKB74svmn_pw1sdZb")

@scan_api.route("/api/v1/sensor-scans", methods=["POST"])
def process_scan():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    try:
        device_id = data["device_id"]
        rfid_code = data["rfid_code"]

        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"error": "API key is required"}), 401

        success = scan_service.process_scan(device_id, rfid_code, api_key)

        if success:
            return jsonify({"message": "Scan registered successfully"}), 200
        else:
            return jsonify({"error": "Scan failed"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
