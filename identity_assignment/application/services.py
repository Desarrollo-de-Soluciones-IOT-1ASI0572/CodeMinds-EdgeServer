import requests
import logging
from typing import Optional, List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class ScanProcessingService:
    """Service for processing RFID scans at the Edge."""

    def __init__(self, base_url: str = "http://localhost:8080/api/v1"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def get_wristband_id(self, rfid_code: str) -> Optional[int]:
        """Fetch wristband ID from backend by RFID code."""
        try:
            url = f"{self.base_url}/wristbands/rfid/{rfid_code}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                wristband = response.json()
                if wristband.get("wristbandStatus") == "ACTIVE":
                    return wristband.get("id")
                logger.warning(f"Wristband {wristband.get('id')} is not ACTIVE")
            else:
                logger.error(f"RFID lookup failed: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching wristband: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        return None

    def send_scan(self, wristband_id: int, scan_type: str) -> bool:
        """Send scan data to backend."""
        if scan_type not in ("ENTRY", "EXIT"):
            logger.error(f"Invalid scan type: {scan_type}")
            return False

        payload = {
            "scanType": scan_type,
            "wristbandId": wristband_id,
            "timestamp": datetime.now().isoformat()
        }

        try:
            url = f"{self.base_url}/sensor-scans/create"
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=5
            )

            if response.ok:
                logger.info(f"Scan recorded for wristband {wristband_id}")
                return True

            logger.error(f"Scan failed: {response.status_code} - {response.text}")
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error sending scan: {e}")
            return False

    def process_scan(self, rfid_code: str, scan_type: str) -> bool:
        """Orchestrate complete scan processing."""
        wristband_id = self.get_wristband_id(rfid_code)
        if wristband_id is None:
            logger.warning(f"No active wristband found for RFID: {rfid_code}")
            return False

        return self.send_scan(wristband_id, scan_type)

    def get_all_scans(self) -> List[Dict]:
        """Retrieve all scan records."""
        try:
            url = f"{self.base_url}/sensor-scans"
            response = requests.get(url, headers=self.headers, timeout=5)

            if response.ok:
                return response.json()

            logger.error(f"Failed to fetch scans: {response.status_code}")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching scans: {e}")
            return []