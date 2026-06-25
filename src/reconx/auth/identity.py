from pydantic import BaseModel


class IdentityContext(BaseModel):
    user_id: str
    tenant_id: str | None = None
    roles: list[str] = []
    permissions: list[str] = []
    session_id: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None

    @property
    def is_super_admin(self) -> bool:
        return "SUPER_ADMIN" in self.roles
