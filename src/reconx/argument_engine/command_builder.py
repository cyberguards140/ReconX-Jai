import logging
from typing import Dict, Any, List

def build_command(binary: str, schema: List[Dict], selections: Dict[str, Any], target: str = "") -> str:
    cmd_parts = [binary]
    
    # Simple compatibility checks
    if selections.get('-active') and selections.get('-passive'):
        raise ValueError("Incompatible Arguments: Cannot use active and passive mode simultaneously")
        
    for arg in schema:
        flag = arg["flag"]
        if flag in selections:
            val = selections[flag]
            arg_type = arg["type"]
            
            if arg_type == "toggle" and val is True:
                cmd_parts.append(flag)
            elif arg_type == "multiselect" and isinstance(val, list) and val:
                cmd_parts.append(f"{flag} {','.join(val)}")
            elif arg_type in ["text", "number", "file", "dropdown"] and val:
                # Handle args without dashes
                if not flag.startswith("-"):
                    cmd_parts.append(str(val))
                else:
                    cmd_parts.append(f"{flag} {val}")

    if target:
        cmd_parts.append(target)
        
    return " ".join(cmd_parts)
