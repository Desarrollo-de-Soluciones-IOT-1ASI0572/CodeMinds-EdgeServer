from iam.application.services import AuthApplicationService
import requests


class ScanProcessingService:
    """Service for processing RFID scans at the Edge."""

    def __init__(self):
        self.iam_service = AuthApplicationService()
        self.base_url = "http://localhost:8080/api/v1"
        self.headers = {"Content-Type": "application/json"}

    def get_wristband_id(self, rfid_code: str) -> int | None:
        """Fetch wristband ID from backend by RFID code.

        Args:
            rfid_code (str): The RFID code scanned.

        Returns:
            int | None: The wristband ID if found, else None.
        """
        try:
            url = f"{self.base_url}/wristbands/rfid/{rfid_code}"
            response = requests.get(url)
            if response.status_code == 200:
                wristband = response.json()
                if wristband["wristbandStatus"] == "ACTIVE":
                    return wristband["id"]
                else:
                    print(f"[GET] Wristband {wristband['id']} is not ACTIVE.")
            else:
                print(f"[GET] RFID {rfid_code} not found. Status: {response.status_code}")
        except Exception as e:
            print(f"[GET] Error fetching wristband ID: {e}")
        return None

    def send_scan(self, wristband_id: int, scan_type: str) -> bool:
        """Send the scan to the backend.

        Args:
            wristband_id (int): The wristband ID.
            scan_type (str): ENTRY or EXIT.

        Returns:
            bool: True if successful, False otherwise.
        """
        payload = {
            "scanType": scan_type,
            "wristbandId": wristband_id
        }

        try:
            url = f"{self.base_url}/sensor-scans/create"
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code in range(200, 300):
                print(f"[POST] Scan registered for wristband ID {wristband_id}")
                return True
            else:
                print(f"[POST] Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[POST] Exception: {e}")
        return False

    def process_scan(self, rfid_code: str, scan_type: str, api_key: str) -> bool:
        """Main method to handle scan processing.

        Args:
            rfid_code (str): The RFID code scanned.
            scan_type (str): ENTRY or EXIT.
            api_key (str): API key for authentication.

        Returns:
            bool: True if scan was successful, False otherwise.
        """
        if not self.iam_service.validate_api_key(api_key):
            print("[AUTH] Invalid API key.")
            return False

        wristband_id = self.get_wristband_id(rfid_code)
        if wristband_id is None:
            print(f"[PROCESS] No valid wristband for RFID: {rfid_code}")
            return False

        return self.send_scan(wristband_id=wristband_id, scan_type=scan_type)
