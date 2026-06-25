import sqlite3

conn = sqlite3.connect('/home/kali/ReconX/product/reconx.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in c.fetchall()]

for table in tables:
    if table != "alembic_version" and not table.startswith('sqlite_'):
        try:
            c.execute(f"ALTER TABLE {table} ADD COLUMN tenant_id VARCHAR(36)")
            print(f"Added tenant_id to {table}")
        except sqlite3.OperationalError as e:
            print(f"Skipped {table}: {e}")

c.execute("CREATE INDEX IF NOT EXISTS ix_assets_tenant_id ON assets (tenant_id)")
# Try to create indices for other tables if necessary

conn.commit()
conn.close()
