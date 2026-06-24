import sqlite3
import uuid
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workspace', 'reconx.db')

class RelationshipEngine:
    def create_relationship(self, parent_id, child_id, rel_type):
        rel_id = str(uuid.uuid4())
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Deduplicate
        cursor.execute("SELECT rel_id FROM relationships WHERE parent_id = ? AND child_id = ? AND rel_type = ?", (parent_id, child_id, rel_type))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO relationships VALUES (?, ?, ?, ?)", (rel_id, parent_id, child_id, rel_type))
            conn.commit()
            
        conn.close()
        return rel_id
