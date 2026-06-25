from typing import Any

from core.auth.identity import IdentityContext
from core.auth.policies import allow


def authorize(
    identity: IdentityContext, permission: str, resource: dict[str, Any] | None = None
) -> tuple[bool, str]:
    """
    Main entry point for the Authorization Engine.
    Evaluates permissions based on IdentityContext, RBAC, and ABAC policies.

    Returns:
        Tuple[bool, str]: (is_allowed, reason)
    """
    # 1. SUPER_ADMIN check
    if identity.is_super_admin:
        return True, "Allowed by SUPER_ADMIN role"

    # 2. Base Permission Check (RBAC)
    if permission not in identity.permissions:
        return False, f"Denied: Missing required permission '{permission}'"

    # 3. Policy Engine Check (ABAC and Tenant Isolation)
    if not allow(identity, permission, resource):
        return False, "Denied: Blocked by ABAC policy or Tenant isolation rules"

    return True, "Allowed"
