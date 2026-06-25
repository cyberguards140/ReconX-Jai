import re


class Validator:
    @staticmethod
    def validate_argument(arg_type, value):
        if value is None or str(value).strip() == "":
            return True  # Empty is handled by required check if needed

        value = str(value)

        if arg_type == "toggle":
            return value.lower() in ["true", "false", "1", "0"]

        if arg_type == "number":
            return value.isdigit()

        if arg_type == "ports":
            # Simple port validation
            return bool(re.match(r"^[\d,\-]+$", value))

        if arg_type == "target":
            # Very loose domain/IP/CIDR check for MVP
            return not bool(re.search(r'[<>!@#$%^&*()_+={}\[\]|\\;:"\',?~]', value))

        return True
