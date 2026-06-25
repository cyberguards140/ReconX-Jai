from typing import List, Optional
from pydantic import BaseModel

class IdentityContext(BaseModel):
    user_id: str
    tenant_id: Optional[str] = None
    roles: List[str] = []
    permissions: List[str] = []
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    @property
    def is_super_admin(self) -> bool:
        return "SUPER_ADMIN" in self.roles
