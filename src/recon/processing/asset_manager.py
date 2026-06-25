import os
import sqlite3
import uuid

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "reconx.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS assets (
            asset_id TEXT PRIMARY KEY,
            asset_type TEXT,
            value TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS domains (asset_id TEXT PRIMARY KEY, domain TEXT);
        CREATE TABLE IF NOT EXISTS subdomains (asset_id TEXT PRIMARY KEY, subdomain TEXT);
        CREATE TABLE IF NOT EXISTS ips (asset_id TEXT PRIMARY KEY, ip TEXT);
        CREATE TABLE IF NOT EXISTS ports (asset_id TEXT PRIMARY KEY, ip_id TEXT, port INTEGER);
        CREATE TABLE IF NOT EXISTS services (asset_id TEXT PRIMARY KEY, port_id TEXT, service TEXT);
        CREATE TABLE IF NOT EXISTS technologies (asset_id TEXT PRIMARY KEY, tech TEXT);
        CREATE TABLE IF NOT EXISTS urls (asset_id TEXT PRIMARY KEY, url TEXT);
        CREATE TABLE IF NOT EXISTS findings (
            finding_id TEXT PRIMARY KEY,
            asset_id TEXT,
            severity TEXT,
            name TEXT,
            description TEXT
        );
        CREATE TABLE IF NOT EXISTS certificates (asset_id TEXT PRIMARY KEY, cn TEXT, issuer TEXT);
        CREATE TABLE IF NOT EXISTS relationships (
            rel_id TEXT PRIMARY KEY,
            parent_id TEXT,
            child_id TEXT,
            rel_type TEXT
        );
        CREATE TABLE IF NOT EXISTS jobs (job_id TEXT PRIMARY KEY);
        CREATE TABLE IF NOT EXISTS metadata (asset_id TEXT PRIMARY KEY, data TEXT);
    """)
    conn.commit()
    conn.close()


class AssetManager:
    def __init__(self):
        init_db()

    def create_asset(self, asset_type, value):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check deduplication
        cursor.execute(
            "SELECT asset_id FROM assets WHERE asset_type = ? AND value = ?", (asset_type, value)
        )
        row = cursor.fetchone()
        if row:
            conn.close()
            return row[0]

        asset_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO assets VALUES (?, ?, ?)", (asset_id, asset_type, value))

        if asset_type == "domain":
            cursor.execute("INSERT INTO domains VALUES (?, ?)", (asset_id, value))
        elif asset_type == "subdomain":
            cursor.execute("INSERT INTO subdomains VALUES (?, ?)", (asset_id, value))
        elif asset_type == "ip":
            cursor.execute("INSERT INTO ips VALUES (?, ?)", (asset_id, value))
        elif asset_type == "url":
            cursor.execute("INSERT INTO urls VALUES (?, ?)", (asset_id, value))

        conn.commit()
        conn.close()
        return asset_id

    def add_finding(self, asset_id, severity, name, description):
        finding_id = str(uuid.uuid4())
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO findings VALUES (?, ?, ?, ?, ?)",
            (finding_id, asset_id, severity, name, description),
        )
        conn.commit()
        conn.close()
        return finding_id
