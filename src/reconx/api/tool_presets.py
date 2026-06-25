import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from argument_engine.presets import get_presets


def get_tool_presets(tool_id):
    presets = get_presets(tool_id)
    return presets
