class RBACCore:
    @staticmethod
    def check_permission(user_role: str, action: str) -> bool:
        matrix = {
            "Viewer": ["View_Assets"],
            "Operator": ["View_Assets", "Run_Jobs"],
            "Admin": ["View_Assets", "Run_Jobs", "Manage_Users"]
        }
        return action in matrix.get(user_role, [])
