import requests
from flask import Blueprint, request, jsonify
from identity_assignment.application.services import ScanProcessingService

scan_api = Blueprint("scan_api", __name__)
scan_service = ScanProcessingService()

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

#@scan_api.route("/api/v1/sensor-scans/<rfid_code>", methods=["GET"])
#def get_scan(rfid_code):
#    try:
#        wristband_id = scan_service.get_wristband_id(rfid_code)
#        if wristband_id:
#            return jsonify({"wristbandId": wristband_id, "message": "Wristband found"}), 200
#        else:
#            return jsonify({"error": "Wristband not found"}), 404
#    except Exception as e:
#        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@scan_api.route("/api/v1/sensor-scans", methods=["GET"])
def get_all_scans():
    try:
        scans = scan_service.get_all_scans()
        return jsonify(scans), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500