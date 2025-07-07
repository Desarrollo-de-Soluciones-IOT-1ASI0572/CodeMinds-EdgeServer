from iam.infrastructure.models import Device


class AuthApplicationService:
    def register_device(self, device_id: str):

        # Genera api_key única
        api_key = "secret-api-key"

        device = Device.create(
            device_id=device_id,
            api_key=api_key
        )
        return device

    def get_device_by_id_and_key(self, device_id: str, api_key: str):
        return Device.get_or_none(Device.device_id == device_id, Device.api_key == api_key)
    
    def get_device_by_id(self, device_id: str):
        """Get device by device_id code only."""
        return Device.get_or_none(Device.device_id == device_id)

