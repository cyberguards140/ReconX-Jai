import re


def validate_input(arg_def, user_input):
    arg_type = arg_def.get("type")

    if arg_def.get("required") and not user_input and user_input is not False:
        return False, "Input is required"

    if not user_input and user_input is not False:
        return True, ""

    if arg_type == "number":
        try:
            int(user_input)
            return True, ""
        except ValueError:
            return False, "Must be a valid number"

    if arg_type == "dropdown":
        options = arg_def.get("options", [])
        if user_input not in options:
            return False, "Invalid option selected"

    if arg_type == "multiselect":
        options = arg_def.get("options", [])
        if not isinstance(user_input, list):
            return False, "Must be a list"
        for item in user_input:
            if item not in options:
                return False, f"Invalid option selected: {item}"

    if arg_type == "toggle":
        if not isinstance(user_input, bool):
            return False, "Must be a boolean value"

    # Basic IP/Domain validation for specific flags
    if arg_def.get("flag") == "-p":
        if not re.match(r"^[\d,\-]+$|top-\d+", str(user_input)):
            return False, "Invalid port format"

    return True, ""
