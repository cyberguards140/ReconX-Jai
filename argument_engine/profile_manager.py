import json
import os
import logging

PROFILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'profiles')
os.makedirs(PROFILES_DIR, exist_ok=True)

def save_profile(name, tool_id, selections):
    filepath = os.path.join(PROFILES_DIR, f"{name.replace(' ', '_').lower()}.json")
    profile = {
        "name": name,
        "tool": tool_id,
        "selections": selections
    }
    with open(filepath, 'w') as f:
        json.dump(profile, f, indent=2)
    logging.info(f"Saved profile: {name} for tool: {tool_id}")

def load_profiles():
    profiles = []
    if not os.path.exists(PROFILES_DIR):
        return profiles
        
    for filename in os.listdir(PROFILES_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(PROFILES_DIR, filename), 'r') as f:
                profiles.append(json.load(f))
    return profiles
