import os
import json

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')

class DashboardCache:
    def write_cache(self, key, data):
        with open(os.path.join(CACHE_DIR, f"{key}.json"), 'w') as f:
            json.dump(data, f)
            
    def read_cache(self, key):
        path = os.path.join(CACHE_DIR, f"{key}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None
