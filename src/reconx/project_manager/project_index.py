import sqlite3
import os
import uuid
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'workspace', 'projects.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            name TEXT UNIQUE,
            status TEXT,
            created_at TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS project_state (
            project_id TEXT PRIMARY KEY,
            state_json TEXT
        );
        CREATE TABLE IF NOT EXISTS project_metadata (
            project_id TEXT PRIMARY KEY,
            metadata_json TEXT
        );
        CREATE TABLE IF NOT EXISTS project_activity (
            activity_id TEXT PRIMARY KEY,
            project_id TEXT,
            activity_type TEXT,
            timestamp TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS project_history (
            history_id TEXT PRIMARY KEY,
            project_id TEXT,
            scan_data TEXT
        );
        CREATE TABLE IF NOT EXISTS project_tags (
            project_id TEXT,
            tag TEXT
        );
    ''')
    conn.commit()
    conn.close()

class ProjectIndex:
    def __init__(self):
        init_db()

    def create_project_record(self, name, tags=None):
        project_id = str(uuid.uuid4())
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("INSERT INTO projects VALUES (?, ?, ?, ?)", (project_id, name, 'active', now))
        
        if tags:
            for tag in tags:
                cursor.execute("INSERT INTO project_tags VALUES (?, ?)", (project_id, tag))
                
        conn.commit()
        conn.close()
        return project_id
