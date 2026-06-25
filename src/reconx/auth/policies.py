from reconx.auth.identity import IdentityContext
from typing import Any, Dict, Optional

def allow(identity: IdentityContext, action: str, resource: Optional[Dict[str, Any]] = None) -> bool:
    """
    Evaluate ABAC policies based on identity, action, and resource attributes.
    Returns True if allowed, False if denied.
    """
    if identity.is_super_admin:
        return True

    # 1. Tenant Isolation Policy
    if resource and "tenant_id" in resource:
        if resource["tenant_id"] and resource["tenant_id"] != identity.tenant_id:
            return False

    # 2. Context-aware policies per role
    if "ANALYST" in identity.roles:
        # Analysts cannot perform deletion actions
        if action.endswith(".delete"):
            return False
            
    if "EXECUTIVE" in identity.roles:
        # Executives primarily view reports and dashboards
        if not action.startswith("report.") and not action.startswith("dashboard.") and not action.endswith(".read"):
            return False
                
    if "AUDITOR" in identity.roles:
        # Auditors have read-only access to everything
        if not action.endswith(".read") and not action.endswith(".export"):
            return False

    return True
