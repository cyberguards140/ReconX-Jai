import os
import re

def replace_in_file(path, replacements):
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(path, 'w') as f:
        f.write(content)

# 1. assets.py (API)
replace_in_file("src/reconx/api/routes/assets.py", [
    ("res = await db.execute(select(Finding))", "res = await finding_repo.get_multi(db)"),
    ("return res.scalars().all()", "return res"),
    ("from sqlalchemy import select", "from reconx.database.repositories.finding import finding_repo"),
    ("from reconx.database.models import Finding", "")
])

# 2. assets.py (CLI)
replace_in_file("src/reconx/cli/assets.py", [
    ("res = await db.execute(select(Finding))", "res = await finding_repo.get_multi(db)"),
    ("findings = res.scalars().all()", "findings = res"),
    ("from sqlalchemy import select", "from reconx.database.repositories.finding import finding_repo"),
    ("from reconx.database.models import Finding", "")
])

# 3. plugins.py (API)
replace_in_file("src/reconx/api/routes/plugins.py", [
    ("result = await db.execute(", "result = await db.execute("), # Actually wait, this is raw execute, I need to see what it's executing. Let's leave for manual.
])

# 4. dashboard_service.py
replace_in_file("src/reconx/reporting/dashboard_service.py", [
    ("assets_res = await self.db.execute(select(Asset))", "assets_res = await asset_repo.get_multi(self.db)"),
    ("assets = assets_res.scalars().all()", "assets = assets_res"),
    ("findings_res = await self.db.execute(select(Finding))", "findings_res = await finding_repo.get_multi(self.db)"),
    ("findings = findings_res.scalars().all()", "findings = findings_res"),
    ("from sqlalchemy import select", "from reconx.database.repositories.asset import asset_repo\nfrom reconx.database.repositories.finding import finding_repo")
])

# 5. state_manager.py
replace_in_file("src/reconx/workflow/state_manager.py", [
    ("self.db.add(exec_record)", "await execution_record_repo.create(self.db, obj_in=exec_record.__dict__)"),
    ("result = await self.db.execute(", "result = await self.db.execute("), # Needs manual check
])

print("Refactoring script applied where possible.")
