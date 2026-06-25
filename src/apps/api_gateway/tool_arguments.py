import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.argument_engine.argument_loader import load_tool_arguments


def get_tool_arguments(tool_id):
    args = load_tool_arguments(tool_id)
    return {"arguments": args}
