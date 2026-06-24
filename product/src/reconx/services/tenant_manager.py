from reconx.modules.enterprise.tenancy import TenancyCore

class TenantManagerService:
    @staticmethod
    def verify_access(user_tenant: str, target_tenant: str) -> bool:
        return TenancyCore.validate_isolation(user_tenant, target_tenant)
