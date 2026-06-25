import os
import re

SRC_DIR = "/home/kali/ReconX/src"

subs = [
    (r"core\.legacy_core\.legacy_core\.legacy_core", "core.legacy_core"),
    (r"core\.legacy_core\.legacy_core", "core.legacy_core"),
    (r"platform\.legacy_platform\.legacy_platform\.legacy_platform", "platform.legacy_platform"),
    (r"platform\.legacy_platform\.legacy_platform", "platform.legacy_platform"),
]

def fix_dupes():
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
    fix_dupes()
    print("[*] Dupes fixed!")
