import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workspace', 'reconx.db')

class MetricsEngine:
    def get_overview_counts(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            counts = {}
            for atype in ['domain', 'subdomain', 'ip', 'url', 'port', 'finding']:
                cursor.execute("SELECT COUNT(*) FROM assets WHERE asset_type = ?", (atype,))
                counts[f"total_{atype}s"] = cursor.fetchone()[0]
                
            conn.close()
            return counts
        except Exception as e:
            return {}
