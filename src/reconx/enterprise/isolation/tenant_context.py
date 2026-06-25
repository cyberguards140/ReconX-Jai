from contextvars import ContextVar
from typing import Optional

# Global context variable to store the current Tenant ID.
# This will be set by a middleware or dependency during the request lifecycle.
_current_tenant_id: ContextVar[Optional[str]] = ContextVar("current_tenant_id", default=None)
_is_super_admin: ContextVar[bool] = ContextVar("is_super_admin", default=False)

def set_current_tenant_id(tenant_id: Optional[str]) -> None:
    """Sets the tenant ID for the current execution context."""
    _current_tenant_id.set(tenant_id)

def get_current_tenant_id() -> Optional[str]:
    """Retrieves the tenant ID for the current execution context."""
    return _current_tenant_id.get()

def set_is_super_admin(is_super: bool) -> None:
    """Sets the super admin bypass flag for the current execution context."""
    _is_super_admin.set(is_super)

def is_super_admin() -> bool:
    """Retrieves whether the current context is executing as a super admin."""
    return _is_super_admin.get()
