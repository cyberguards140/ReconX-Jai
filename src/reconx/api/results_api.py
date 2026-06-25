import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'workspace', 'reconx.db')

class ResultsAPI:
    def handle_request(self, method, path):
        parts = path.strip('/').split('/')
        if len(parts) >= 2 and parts[0] == 'api':
            
            if parts[1] == 'assets' and method == 'GET':
                return self.get_all("assets")
            elif parts[1] == 'findings' and method == 'GET':
                return self.get_all("findings")
            elif parts[1] == 'technologies' and method == 'GET':
                return self.get_all("technologies")
            elif parts[1] == 'relationships' and method == 'GET':
                return self.get_all("relationships")
            
        return {"error": "Invalid results endpoint"}
        
    def get_all(self, table):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} LIMIT 100")
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            return {"error": str(e)}
