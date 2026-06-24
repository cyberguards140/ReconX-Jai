import re
from typing import Dict, Any, List, Tuple

class CypherBuilder:
    """
    Safely builds Cypher queries with parameters to prevent injection.
    """
    def __init__(self):
        self.query_parts: List[str] = []
        self.parameters: Dict[str, Any] = {}
        self.param_counter = 0

    def match_node(self, label: str, variable: str = "n", properties: Dict[str, Any] = None) -> 'CypherBuilder':
        if not re.match(r"^[A-Za-z0-9_]+$", label) or not re.match(r"^[A-Za-z0-9_]+$", variable):
            raise ValueError("Invalid label or variable name")
        
        prop_str = ""
        if properties:
            prop_parts = []
            for k, v in properties.items():
                if not re.match(r"^[A-Za-z0-9_]+$", k):
                    raise ValueError("Invalid property key")
                param_name = f"p_{self.param_counter}"
                self.param_counter += 1
                self.parameters[param_name] = v
                prop_parts.append(f"{k}: ${param_name}")
            prop_str = f" {{{', '.join(prop_parts)}}}"

        self.query_parts.append(f"MATCH ({variable}:{label}{prop_str})")
        return self

    def return_vars(self, *variables: str) -> 'CypherBuilder':
        for var in variables:
            if not re.match(r"^[A-Za-z0-9_]+$", var):
                raise ValueError("Invalid variable name")
        
        self.query_parts.append(f"RETURN {', '.join(variables)}")
        return self

    def limit(self, max_records: int) -> 'CypherBuilder':
        self.query_parts.append(f"LIMIT {int(max_records)}")
        return self

    def skip(self, offset: int) -> 'CypherBuilder':
        self.query_parts.append(f"SKIP {int(offset)}")
        return self

    def build(self) -> Tuple[str, Dict[str, Any]]:
        return "\n".join(self.query_parts), self.parameters
