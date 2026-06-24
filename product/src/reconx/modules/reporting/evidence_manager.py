import json
import os

class EvidenceManager:
    """Stores raw evidence mapping to finding IDs."""
    
    def __init__(self, storage_dir="/tmp/reconx_evidence"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        
    def store_evidence(self, finding_id: str, raw_content: str) -> str:
        file_path = os.path.join(self.storage_dir, f"{finding_id}.txt")
        with open(file_path, "w") as f:
            f.write(raw_content)
        return file_path
        
    def get_evidence(self, finding_id: str) -> str:
        file_path = os.path.join(self.storage_dir, f"{finding_id}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return f.read()
        return ""
