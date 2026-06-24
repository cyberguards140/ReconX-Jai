import shutil
import logging
import sqlite3
import os

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workspace')
os.makedirs(CACHE_DIR, exist_ok=True)

def check_dependencies(dependencies):
    logging.info("Checking dependencies...")
    
    db_path = os.path.join(CACHE_DIR, 'tool_cache.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tool_status 
                      (tool_id TEXT PRIMARY KEY, status TEXT, install_method TEXT)''')
    
    for dep in dependencies:
        tid = dep['tool']
        binary = dep['binary']
        install_method = dep.get('install_method', 'unknown')
        
        path = shutil.which(binary)
        status = "installed" if path else "missing"
        
        cursor.execute('''INSERT OR REPLACE INTO tool_status 
                          (tool_id, status, install_method) VALUES (?, ?, ?)''', 
                       (tid, status, install_method))
        
        if status == "missing":
            logging.warning(f"Dependency missing: {binary} for tool {tid}")
        else:
            logging.debug(f"Dependency found: {binary} at {path}")
            
    conn.commit()
    conn.close()
    logging.info("Dependency check complete.")
