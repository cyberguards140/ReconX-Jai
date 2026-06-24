import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from argument_engine.profile_manager import load_profiles

def get_tool_profiles(tool_id):
    profiles = load_profiles()
    tool_profiles = [p for p in profiles if p.get('tool') == tool_id]
    return tool_profiles
