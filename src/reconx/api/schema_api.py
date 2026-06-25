from .tool_arguments import get_tool_arguments
from .tool_presets import get_tool_presets
from .tool_profiles import get_tool_profiles


class SchemaAPI:
    def handle_request(self, method, path):
        parts = path.strip("/").split("/")
        if len(parts) >= 4 and parts[0] == "api" and parts[1] == "tools":
            tool_id = parts[2]
            endpoint = parts[3]

            if endpoint == "arguments":
                return get_tool_arguments(tool_id)
            elif endpoint == "presets":
                return get_tool_presets(tool_id)
            elif endpoint == "profiles":
                return get_tool_profiles(tool_id)

        return {"error": "Invalid endpoint"}
