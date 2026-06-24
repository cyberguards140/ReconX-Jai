from reconx.modules.enterprise.rbac import RBACCore

class RBACService:
    @staticmethod
    def authorize(role: str, action: str) -> bool:
        return RBACCore.check_permission(role, action)
