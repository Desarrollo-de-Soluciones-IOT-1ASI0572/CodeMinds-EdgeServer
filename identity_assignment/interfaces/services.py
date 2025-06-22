from flask import Blueprint, request, jsonify
from identity_assignment.application.services import ScanProcessingService

scan_api = Blueprint("scan_api", __name__)
scan_service = ScanProcessingService(token="eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhc2Rhc2QxMjMiLCJpYXQiOjE3NTA1Njc2NTcsImV4cCI6MTc1MTE3MjQ1N30.76E_-F-bFd5513aAkCx355Vsvooq5ET3jxMPHvD7PpNuRAI6OF_GVsTHu049a-8y")  # Initialize with no token for simplicity

@scan_api.route("/api/v1/sensor-scans/create", methods=["POST"])
def process_scan():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    try:
        rfid_code = data["rfidCode"]
        scan_type = data["scanType"]

        success = scan_service.process_scan(rfid_code, scan_type)

        if success:
            return jsonify({"message": "Scan registered successfully"}), 200
        else:
            return jsonify({"error": "Scan failed"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
