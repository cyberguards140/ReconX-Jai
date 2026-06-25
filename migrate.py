import os
import re
import shutil

SRC_DIR = "/home/kali/ReconX/src"
RECONX_DIR = os.path.join(SRC_DIR, "reconx")

# Mapping of current reconx/<folder> to the new <domain>/<subfolder>
MAPPING = {
    # Apps
    "cli": "apps/cli",
    "dashboard": "apps/dashboard",
    "api": "apps/api_gateway",
    "api_gateway": "apps/api_gateway/gateway",
    "command_center": "apps/command_center",
    "frontend": "apps/dashboard/frontend",  # Moving frontend here
    # Core
    "config": "core/config",
    "auth": "core/auth",
    "cache": "core/cache",
    "events": "core/events",
    "core": "core/legacy_core",  # moving the generic core folder
    "argument_engine": "core/argument_engine",
    # Platform
    "workflows": "platform/workflow_engine/workflows",
    "workflow": "platform/workflow_engine/workflow",
    "plugins": "platform/plugin_engine",
    "rules": "platform/rule_engine",
    "execution": "platform/task_engine/execution",
    "pipeline_engine": "platform/task_engine/pipeline_engine",
    "pipelines": "platform/task_engine/pipelines",
    "platform": "platform/legacy_platform",
    "state": "platform/orchestration/state",
    # AI
    "ai": "ai",
    "autonomous": "ai/agents/autonomous",
    "agents": "ai/agents",
    "prompts": "ai/prompts",
    # Graph
    "graph": "graph",
    # Operations
    "project_manager": "operations/projects/manager",
    "projects": "operations/projects",
    "doctor": "operations/runbooks/doctor",
    # Intelligence & Recon
    "global_intel": "intelligence/global_intel",
    "modules": "recon/modules",
    "services": "recon/services",
    "processing": "recon/processing",
    "parsers": "recon/parsers",
    # Vulnerability & Attack Surface
    "digital_twin": "attack_surface/assets",
    # Reporting
    "reporting": "reporting",
    "templates": "reporting/templates",
    "output": "reporting/output",
    # Integrations
    "integrations": "integrations",
    "tool_manager": "integrations/tool_manager",
    "adapters": "integrations/adapters",
    # Observability
    "observability": "observability",
    "metrics": "observability/metrics",
    "logs": "observability/logging",
    # Data
    "database": "data/database",
    "data_fabric": "data/data_fabric",
    "schemas": "data/schemas",
    # Enterprise & SaaS & Security
    "enterprise": "plugins/enterprise",
    "saas": "plugins/saas",
    "security": "security",
    # Internet Scale
    "distributed": "recon/internet_scale/distributed",
    "streaming": "recon/internet_scale/streaming",
    # Misc & Archive
    "utils": "archive/deprecated/utils",
    "meta": "archive/deprecated/meta",
    "workspace": "archive/deprecated/workspace",
}


def create_init_files(base_path):
    """Ensure __init__.py exists in all newly created python package directories."""
    for root, dirs, files in os.walk(base_path):
        if "__init__.py" not in files and not root.endswith("__pycache__"):
            # Don't create __init__.py if it's just a data directory, but we assume src/* are packages
            open(os.path.join(root, "__init__.py"), "a").close()


def move_directories():
    print("[*] Moving directories to domain structure...")
    for old_name, new_path in MAPPING.items():
        old_dir = os.path.join(RECONX_DIR, old_name)
        new_dir = os.path.join(SRC_DIR, new_path)

        if os.path.exists(old_dir):
            os.makedirs(os.path.dirname(new_dir), exist_ok=True)
            print(f"Moving {old_name} -> {new_path}")
            shutil.move(old_dir, new_dir)

    # Move specific files in reconx root
    for f in [
        "__init__.py",
        "__main__.py",
        "main.py",
        "logger.py",
        "version.py",
        "dashboard_state.json",
    ]:
        old_f = os.path.join(RECONX_DIR, f)
        if os.path.exists(old_f):
            if f in ["__main__.py", "main.py"]:
                # Let's put main entry points in apps/cli
                os.makedirs(os.path.join(SRC_DIR, "apps/cli"), exist_ok=True)
                shutil.move(old_f, os.path.join(SRC_DIR, "apps/cli", f))
            elif f == "logger.py":
                os.makedirs(os.path.join(SRC_DIR, "core/logging"), exist_ok=True)
                shutil.move(old_f, os.path.join(SRC_DIR, "core/logging", f))
            elif f == "version.py":
                os.makedirs(os.path.join(SRC_DIR, "core/constants"), exist_ok=True)
                shutil.move(old_f, os.path.join(SRC_DIR, "core/constants", f))
            else:
                shutil.move(old_f, os.path.join(SRC_DIR, "core", f))


def rewrite_imports():
    print("[*] Rewriting import statements across codebase...")

    subs = []
    for old_name, new_path in MAPPING.items():
        new_module = new_path.replace("/", ".")

        # from reconx.old_name.something -> from new_module.something
        subs.append((rf"from reconx\.{old_name}\b", f"from {new_module}"))
        subs.append((rf"import reconx\.{old_name}\b", f"import {new_module}"))

        # from old_name.something -> from new_module.something
        subs.append((rf"from {old_name}\b", f"from {new_module}"))

    # Also handle main.py and logger.py re-routes
    subs.append((r"from reconx\.logger\b", "from core.logging.logger"))
    subs.append((r"from reconx\.version\b", "from core.constants.version"))
    subs.append((r"from reconx\.main\b", "from apps.cli.main"))

    # Also handle `reconx.` prefix for things we couldn't map specifically
    subs.append((r"from reconx\b", "from core"))  # fallback

    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, encoding="utf-8") as f:
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
    move_directories()

    # We can delete the empty reconx directory
    if os.path.exists(RECONX_DIR) and not os.listdir(RECONX_DIR):
        os.rmdir(RECONX_DIR)
        print("[*] Removed old reconx directory.")

    create_init_files(SRC_DIR)
    rewrite_imports()
    print("[*] Refactoring complete!")
