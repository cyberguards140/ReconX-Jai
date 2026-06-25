import os
import platform
import psutil

class EnvironmentValidator:
    @staticmethod
    def validate_directories():
        dirs = ['projects', 'logs', 'output', 'templates', 'cache', 'workspace']
        results = []
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        for d in dirs:
            p = os.path.join(base, d)
            if not os.path.exists(p):
                try:
                    os.makedirs(p, exist_ok=True)
                    results.append({"directory": d, "status": "Created", "writable": True})
                except:
                    results.append({"directory": d, "status": "Missing", "writable": False})
            else:
                writable = os.access(p, os.W_OK)
                results.append({"directory": d, "status": "Exists", "writable": writable})
        return results

    @staticmethod
    def validate_system():
        return {
            "os": platform.system(),
            "architecture": platform.machine(),
            "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "cpu_cores": psutil.cpu_count(),
            "python_version": platform.python_version()
        }
