import requests
from iam.application.services import AuthApplicationService
from assignments.infrastructure.repositories import ScanStateRepository

class ScanProcessingService:
    """Service for processing RFID scans at the Edge."""
    def __init__(self, token=None):
        self.auth_service = AuthApplicationService()
        self.scan_state_repository = ScanStateRepository()
        self.base_url = "http://localhost:8080/api/v1"
        self.headers = {
            "Content-Type": "application/json"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def authenticate_device(self, device_id: str, api_key: str):
        """Authenticate device using IAM service."""
        return self.auth_service.get_device_by_id_and_key(device_id, api_key)


    def get_all_scans(self) -> list:
        """Obtiene todos los registros de escaneos desde el backend.

        Returns:
            list: Una lista con todos los registros de escaneos.
        """
        try:
            url = f"{self.base_url}/sensor-scans"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[GET] Error al obtener los escaneos. Estado: {response.status_code}")
                return []
        except Exception as e:
            print(f"[GET] Excepción al obtener los escaneos: {e}")
            return []
            

    def get_wristband_id(self, rfid_code: str) -> int | None:
        """Fetch wristband ID from backend by RFID code.

        Args:
            rfid_code (str): The RFID code scanned.

        Returns:
            int | None: The wristband ID if found, else None.
        """
        try:
            url = f"{self.base_url}/wristbands/rfid/{rfid_code}"
            response = requests.get(url, headers=self.headers)
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
    
    def determine_scan_type(self, wristband_id: int) -> str:
        """Determine scan type based on scan count. Impar = ENTRY, Par = EXIT."""
        try:
            # Get current scan count
            current_count = self.scan_state_repository.get_scan_count_by_wristband_id(wristband_id)
            
            # Next scan number (current + 1)
            next_scan_number = current_count + 1
            
            # Impar = ENTRY, Par = EXIT
            if next_scan_number % 2 == 1:  # Impar
                scan_type = "ENTRY"
            else:  # Par
                scan_type = "EXIT"
            
            print(f"[SCAN_TYPE] Wristband {wristband_id}: scan #{next_scan_number} = {scan_type}")
            
            return scan_type
            
        except Exception as e:
            print(f"[ERROR] Error determining scan type: {e}")
            return "ENTRY"  # Default fallback

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
            url = f"{self.base_url}/sensor-scans"
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code in range(200, 300):
                print(f"[POST] Scan registered for wristband ID {wristband_id}")
                return True
            else:
                print(f"[POST] Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[POST] Exception: {e}")
        return False

    def process_scan(self, device_id: str, rfid_code: str, api_key: str) -> bool:
        """Main method to handle scan processing.

        Args:
            rfid_code (str): The RFID code scanned.
            scan_type (str): ENTRY or EXIT.

        Returns:
            bool: True if scan was successful, False otherwise.
        """
        try:
            device = self.authenticate_device(device_id, api_key)
            if not device:
                raise ValueError("Invalid authentication credentials")
            
            print(f"[AUTH] Device authenticated: {device.device_id}")

            wristband_id = self.get_wristband_id(rfid_code)
            if wristband_id is None:
                print(f"[PROCESS] No valid wristband for RFID: {rfid_code}")
                return False
            
            scan_type = self.determine_scan_type(wristband_id)

            success = self.send_scan(wristband_id=wristband_id, scan_type=scan_type)

            if success:
                    # Increment scan count only if backend call succeeded
                    new_count = self.scan_state_repository.increment_scan_count(wristband_id)
                    print(f"[SCAN_COUNT] Wristband {wristband_id} now has {new_count} scans")
                    return True
            else:
                    print(f"[ERROR] Failed to send scan to backend")
                    return False
        
        except ValueError as e:
            print(f"[ERROR] ValueError: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return False
