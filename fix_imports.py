import os
import re

SRC_DIR = "/home/kali/ReconX/src"

subs = [
    # Fix over-greedy core replacements
    (r"from core\.legacy_core\.auth\b", "from core.auth"),
    (r"import core\.legacy_core\.auth\b", "import core.auth"),
    (r"from core\.legacy_core\.config\b", "from core.config"),
    (r"import core\.legacy_core\.config\b", "import core.config"),
    (r"from core\.legacy_core\.cache\b", "from core.cache"),
    (r"import core\.legacy_core\.cache\b", "import core.cache"),
    (r"from core\.legacy_core\.events\b", "from core.events"),
    (r"import core\.legacy_core\.events\b", "import core.events"),
    (r"from core\.legacy_core\.argument_engine\b", "from core.argument_engine"),
    (r"import core\.legacy_core\.argument_engine\b", "import core.argument_engine"),
    (r"from core\.legacy_core\.logging\b", "from core.logging"),
    (r"from core\.legacy_core\.constants\b", "from core.constants"),
    
    # Fix over-greedy platform replacements
    (r"from platform\.legacy_platform\.workflow_engine\b", "from platform.workflow_engine"),
    (r"import platform\.legacy_platform\.workflow_engine\b", "import platform.workflow_engine"),
    (r"from platform\.legacy_platform\.plugin_engine\b", "from platform.plugin_engine"),
    (r"import platform\.legacy_platform\.plugin_engine\b", "import platform.plugin_engine"),
    (r"from platform\.legacy_platform\.rule_engine\b", "from platform.rule_engine"),
    (r"from platform\.legacy_platform\.task_engine\b", "from platform.task_engine"),
    (r"from platform\.legacy_platform\.orchestration\b", "from platform.orchestration"),
    
    # Just generic fix for trailing dot:
    # Any time it wrote `core.legacy_core` where it should have been `core` because the trailing part was moved to `core`
]

def fix_imports():
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    new_content = content
                    for pattern, repl in subs:
                        new_content = re.sub(pattern, repl, new_content)
                        
                    if new_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Failed to process {filepath}: {e}")

if __name__ == "__main__":
    fix_imports()
    print("[*] Imports fixed!")
