def generate_ui_schema(tool_arguments):
    ui_schema = []
    for arg in tool_arguments:
        ui_elem = {
            "id": f"arg_{arg['flag'].replace('-', '')}",
            "label": arg["name"],
            "type": arg["type"],
            "flag": arg["flag"],
            "default": arg.get("default", ""),
            "required": arg.get("required", False),
        }
        if "options" in arg:
            ui_elem["options"] = arg["options"]
        ui_schema.append(ui_elem)
    return ui_schema
