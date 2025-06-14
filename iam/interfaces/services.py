from flask import Blueprint, request, jsonify
from iam.application.services import AuthApplicationService

iam_api = Blueprint("iam", __name__, url_prefix="/iam")
auth_service = AuthApplicationService()

@iam_api.route("/register", methods=["POST"])
def register_device():
    data = request.json
    student_name = data.get("student_name", None)

    device = auth_service.register_rfid(student_name)

    return jsonify({
        "rfid_code": device.rfid_code,
        "api_key": device.api_key
    }), 201

@iam_api.route("/authenticate", methods=["POST"])
def authenticate_device():
    data = request.json
    rfid_code = data.get("rfid_code")
    api_key = data.get("api_key")

    device = auth_service.get_device_by_code_and_key(rfid_code, api_key)

    if device:
        return jsonify({
            "authenticated": True,
            "rfid_code": device.rfid_code,
            "student_name": device.student_name
        }), 200

    return jsonify({
        "authenticated": False,
        "error": "Invalid credentials"
    }), 401

