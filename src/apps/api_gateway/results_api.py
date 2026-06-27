import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "reconx.db")


class ResultsAPI:
    def handle_request(self, method, path):
        parts = path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "api":
            if parts[1] == "assets" and method == "GET":
                return self.get_all("assets")
            elif parts[1] == "findings" and method == "GET":
                return self.get_all("findings")
            elif parts[1] == "technologies" and method == "GET":
                return self.get_all("technologies")
            elif parts[1] == "relationships" and method == "GET":
                return self.get_all("relationships")

        return {"error": "Invalid results endpoint"}

    def get_all(self, table):
        allowed_tables = {"assets", "findings", "technologies", "relationships"}
        if table not in allowed_tables:
            return {"error": "Invalid table requested"}
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            QUERIES = {
                "assets": "SELECT * FROM assets LIMIT 100",
                "findings": "SELECT * FROM findings LIMIT 100",
                "technologies": "SELECT * FROM technologies LIMIT 100",
                "relationships": "SELECT * FROM relationships LIMIT 100"
            }
            cursor.execute(QUERIES[table])
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            return {"error": str(e)}
