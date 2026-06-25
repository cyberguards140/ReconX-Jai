import shutil


class DependencyChecker:
    @staticmethod
    def check_dependency(cmd, name):
        if not shutil.which(cmd):
            return {"dependency": name, "installed": False}
        return {"dependency": name, "installed": True}

    @staticmethod
    def check_all():
        deps = [
            ("python3", "Python"),
            ("node", "NodeJS"),
            ("npm", "NPM"),
            ("go", "Go"),
            ("git", "Git"),
            ("docker", "Docker"),
            ("sqlite3", "SQLite"),
        ]
        return [DependencyChecker.check_dependency(cmd, name) for cmd, name in deps]
