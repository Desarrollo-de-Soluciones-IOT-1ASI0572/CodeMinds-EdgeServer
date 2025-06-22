import requests

class SensorScanAPI:
    """Handles communication with the backend sensor scan endpoint."""

    def __init__(self):
        self.endpoint_url = "http://localhost:8000/api/v1/sensor-scans/create"  # Cambia si usas otro host
        self.headers = {
            "Content-Type": "application/json"
            # Puedes agregar aquí Authorization si usas JWT: "Authorization": "Bearer <token>"
        }

    def send_scan(self, scan_type: str, wristband_id: int) -> bool:
        """Send a scan event to the backend.

        Args:
            scan_type (str): 'ENTRY' or 'EXIT'
            wristband_id (int): The ID of the wristband associated with the scan.

        Returns:
            bool: True if request was successful (status code 2xx), False otherwise.
        """
        payload = {
            "scanType": scan_type,
            "wristbandId": wristband_id
        }

        try:
            response = requests.post(self.endpoint_url, json=payload, headers=self.headers)
            if response.status_code >= 200 and response.status_code < 300:
                return True
            else:
                print(f"[SensorScanAPI] Error {response.status_code}: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[SensorScanAPI] Exception: {e}")
            return False