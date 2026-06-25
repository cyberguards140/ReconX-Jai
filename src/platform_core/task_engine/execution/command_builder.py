class CommandBuilder:
    def build(self, tool, args):
        command = [tool]
        for key, value in args.items():
            if key == "target":
                continue

            # Simple key mapping for flags
            if len(key) == 1:
                flag = f"-{key}"
            else:
                flag = f"--{key}"

            if isinstance(value, bool):
                if value:
                    command.append(flag)
            elif isinstance(value, list):
                for item in value:
                    command.extend([flag, str(item)])
            else:
                command.extend([flag, str(value)])

        return command
