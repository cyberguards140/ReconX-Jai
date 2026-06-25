from enum import Enum


class Role(Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class RBACEngine:
    """
    Role-Based Access Control logic.
    """

    def __init__(self):
        # Define base permissions per role
        self.permissions: dict[Role, list[str]] = {
            Role.SUPER_ADMIN: ["*"],
            Role.TENANT_ADMIN: [
                "assets:read",
                "assets:write",
                "assets:delete",
                "scans:trigger",
                "scans:cancel",
                "users:invite",
                "users:remove",
            ],
            Role.ANALYST: ["assets:read", "assets:write", "scans:trigger"],
            Role.VIEWER: ["assets:read", "reports:read"],
        }

    def has_permission(self, user_role: str, action: str) -> bool:
        try:
            role = Role(user_role.lower())
        except ValueError:
            return False

        role_perms = self.permissions.get(role, [])
        if "*" in role_perms:
            return True

        return action in role_perms


rbac_engine = RBACEngine()
