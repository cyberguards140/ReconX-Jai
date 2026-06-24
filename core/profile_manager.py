import os
import json

class ProfileManager:
    PROFILES_DIR = "registry/profiles"

    @staticmethod
    def _ensure_dir():
        if not os.path.exists(ProfileManager.PROFILES_DIR):
            os.makedirs(ProfileManager.PROFILES_DIR)

    @staticmethod
    def get_profiles(tool_id):
        # MVP Mock profiles based on request
        if tool_id == "nmap":
            return [
                {"name": "Quick Scan", "config": {"-sV": "true", "-T": "T4", "--top-ports": "100"}},
                {"name": "Full TCP Scan", "config": {"-sV": "true", "-p": "1-65535", "-T": "T4"}},
                {"name": "Aggressive Scan", "config": {"-A": "true", "-T": "T4"}},
                {"name": "Stealth Scan", "config": {"-sS": "true", "-Pn": "true", "-T": "T2"}}
            ]
        return []
