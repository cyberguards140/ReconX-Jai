import json
import logging
import os
from typing import Any

from .category_loader import load_categories
from .dependency_checker import check_dependencies
from .metadata_loader import load_tool_metadata
from .registry_validator import validate_registry

REGISTRY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "registry")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "tool_registry.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class RegistryLoader:
    def __init__(self):
        self.tools = []
        self.categories = []
        self.metadata = []
        self.dependencies = []
        self.outputs = []
        self.adapters = []

    def load_all(self):
        logging.info("Starting Registry Load")
        self.tools = self._load_json("tools.json")
        self.categories = load_categories()
        self.metadata = load_tool_metadata()
        self.dependencies = self._load_json("dependencies.json")
        self.outputs = self._load_json("outputs.json")
        self.adapters = self._load_json("adapters.json")

        logging.info(f"Loaded {len(self.tools)} tools")

        # Validate
        validate_registry(self)

        # Check Dependencies
        check_dependencies(self.dependencies)
        logging.info("Registry Load Complete")

    def _load_json(self, filename: str) -> Any:
        filepath = os.path.join(REGISTRY_DIR, filename)
        if not os.path.exists(filepath):
            logging.error(f"Missing registry file: {filename}")
            return []
        with open(filepath) as f:
            return json.load(f)

    def get_tool(self, tool_id: str) -> dict[str, Any]:
        return next((t for t in self.tools if t["id"] == tool_id), None)
