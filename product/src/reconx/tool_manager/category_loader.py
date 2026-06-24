import json
import os

REGISTRY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'registry')

def load_categories():
    filepath = os.path.join(REGISTRY_DIR, 'categories.json')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []
