import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from integrations.adapters.api_adapter import ApiAdapter
from integrations.adapters.docker_adapter import DockerAdapter
from integrations.adapters.go_adapter import GoAdapter
from integrations.adapters.python_adapter import PythonAdapter
from integrations.adapters.shell_adapter import ShellAdapter


class AdapterManager:
    def __init__(self, process_runner):
        self.adapters = {
            "shell_adapter": ShellAdapter(process_runner),
            "docker_adapter": DockerAdapter(process_runner),
            "python_adapter": PythonAdapter(process_runner),
            "go_adapter": GoAdapter(process_runner),
            "api_adapter": ApiAdapter(process_runner),
        }

    def get_adapter(self, adapter_name):
        return self.adapters.get(adapter_name, self.adapters["shell_adapter"])
