from operations.runbooks.doctor.binary_checker import BinaryChecker
from operations.runbooks.doctor.dependency_checker import DependencyChecker
from operations.runbooks.doctor.environment_validator import EnvironmentValidator


class DoctorEngine:
    @staticmethod
    def scan():
        system_info = EnvironmentValidator.validate_system()
        directories = EnvironmentValidator.validate_directories()
        dependencies = DependencyChecker.check_all()
        binaries = BinaryChecker.check_all()

        missing_tools = [b for b in binaries if not b["installed"]]
        missing_deps = [d for d in dependencies if not d["installed"]]

        status = "Healthy"
        if missing_tools or missing_deps:
            status = "Warning"
            if len(missing_tools) > 5:
                status = "Critical"

        return {
            "status": status,
            "system": system_info,
            "directories": directories,
            "dependencies": dependencies,
            "tools": binaries,
            "missing_tools": [t["tool"] for t in missing_tools],
            "missing_dependencies": [d["dependency"] for d in missing_deps],
        }
