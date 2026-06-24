import os
import shutil
from pathlib import Path

def move_dir_contents(src, dst):
    src_path = Path(src)
    dst_path = Path(dst)
    if not src_path.exists(): return
    dst_path.mkdir(parents=True, exist_ok=True)
    for item in src_path.iterdir():
        if item.name == "__pycache__": continue
        shutil.move(str(item), str(dst_path / item.name))
    shutil.rmtree(src_path)

def replace_imports(old_import, new_import):
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()
                if old_import in content:
                    new_content = content.replace(old_import, new_import)
                    with open(path, "w") as f:
                        f.write(new_content)
    for root, _, files in os.walk("tests"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()
                if old_import in content:
                    new_content = content.replace(old_import, new_import)
                    with open(path, "w") as f:
                        f.write(new_content)

# Database
move_dir_contents("src/reconx/db", "src/reconx/database")
move_dir_contents("src/reconx/core/database", "src/reconx/database")
replace_imports("reconx.core.database", "reconx.database")
replace_imports("reconx.db", "reconx.database")

# Agents
move_dir_contents("src/reconx/agent", "src/reconx/agents")
replace_imports("reconx.agent.", "reconx.agents.")
replace_imports("reconx.agent ", "reconx.agents ")
replace_imports("reconx.agent\n", "reconx.agents\n")

# Plugins
move_dir_contents("src/reconx/core/plugins", "src/reconx/plugins")
move_dir_contents("src/reconx/core/plugin_manager", "src/reconx/plugins")
replace_imports("reconx.core.plugin_manager", "reconx.plugins")
replace_imports("reconx.core.plugins", "reconx.plugins")

# API
move_dir_contents("src/reconx/core/api_gateway", "src/reconx/api")
move_dir_contents("src/reconx/core/api", "src/reconx/api")
replace_imports("reconx.core.api_gateway", "reconx.api")
replace_imports("reconx.core.api", "reconx.api")

# Shrinking core/ -> workflow, events, utils, services
move_dir_contents("src/reconx/core/workflow", "src/reconx/workflow")
replace_imports("reconx.core.workflow", "reconx.workflow")

move_dir_contents("src/reconx/core/events", "src/reconx/events")
replace_imports("reconx.core.events", "reconx.events")

move_dir_contents("src/reconx/core/utils", "src/reconx/utils")
replace_imports("reconx.core.utils", "reconx.utils")

domains = [
    "alerts", "analytics", "asm", "auth", "dashboard", "decision", 
    "defense_analysis", "dependency_manager", "intelligence", 
    "jobs", "mitre_mapping", "observability", "operations", 
    "policies", "strategy", "validation"
]
for domain in domains:
    move_dir_contents(f"src/reconx/core/{domain}", f"src/reconx/services/{domain}")
    replace_imports(f"reconx.core.{domain}", f"reconx.services.{domain}")

print("Migration complete!")
