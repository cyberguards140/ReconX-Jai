import sqlite3
import os
import json
import uuid
import logging
from datetime import datetime

WORKSPACE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workspace')
DB_PATH = os.path.join(WORKSPACE_DIR, 'jobs.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            tool TEXT,
            project TEXT,
            target TEXT,
            arguments TEXT,
            created_at TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS job_status (
            job_id TEXT PRIMARY KEY,
            status TEXT,
            updated_at TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS job_logs (
            job_id TEXT,
            log_entry TEXT,
            timestamp TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS job_errors (
            job_id TEXT,
            error_message TEXT,
            timestamp TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS job_metrics (
            job_id TEXT PRIMARY KEY,
            pid INTEGER,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            duration REAL,
            exit_code INTEGER
        );
    ''')
    conn.commit()
    conn.close()

class JobTracker:
    def __init__(self):
        init_db()
        
    def create_job(self, tool, project, target, arguments):
        job_id = str(uuid.uuid4())
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)",
                       (job_id, tool, project, target, json.dumps(arguments), now))
        cursor.execute("INSERT INTO job_status VALUES (?, ?, ?)",
                       (job_id, "queued", now))
        conn.commit()
        conn.close()
        logging.info(f"Job created: {job_id} for tool {tool}")
        return job_id
        
    def update_status(self, job_id, status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE job_status SET status = ?, updated_at = ? WHERE job_id = ?",
                       (status, datetime.now().isoformat(), job_id))
        conn.commit()
        conn.close()
        logging.info(f"Job {job_id} status updated to {status}")

    def get_job_status(self, job_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM job_status WHERE job_id = ?", (job_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "unknown"
