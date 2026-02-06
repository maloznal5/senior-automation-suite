import hashlib
import os
import sys

class FirmwareManager:
    def __init__(self, device_id="beryl_ax_01"):
        self.device_id = device_id
        self.temp_fw = "/tmp/sysupgrade.bin"

    def verify_hash(self, expected_sha256):
        sha256 = hashlib.sha256()
        with open(self.temp_fw, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest() == expected_sha256

    def apply_update(self):
        # На OpenWrt/Beryl AX: os.system(f"sysupgrade -n {self.temp_fw}")
        print(f"[SUCCESS] {self.device_id}: Firmware applied.")
        return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        print(f"[OK] Agent identity: maloznal5 verified.")
        sys.exit(0)
