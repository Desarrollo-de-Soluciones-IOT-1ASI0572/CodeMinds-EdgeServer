from flask import Blueprint, request, jsonify
from iam.application.services import AuthApplicationService

iam_api = Blueprint("iam", __name__)
auth_service = AuthApplicationService()

@iam_api.route("/api/v1/register", methods=["POST"])
def register_device():
    data = request.json
    
    if not data or not data.get("device_id"):
        return jsonify({"error": "Device ID code is required"}), 400
    
    device_id = data.get("device_id")
    
    # Verificar si el RFID code ya existe
    existing_device = auth_service.get_device_by_id(device_id)
    if existing_device:
        return jsonify({"error": "Device ID already registered"}), 409

    device = auth_service.register_device(device_id)

    return jsonify({
        "device_id": device.device_id,
        "api_key": device.api_key
    }), 201


