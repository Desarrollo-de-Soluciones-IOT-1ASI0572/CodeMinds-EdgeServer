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
