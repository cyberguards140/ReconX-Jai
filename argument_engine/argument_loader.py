import json
import os
import logging

ARGUMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'registry', 'arguments')

def load_tool_arguments(tool_id):
    filepath = os.path.join(ARGUMENTS_DIR, f"{tool_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    logging.warning(f"No argument schema found for tool: {tool_id}")
    return []
