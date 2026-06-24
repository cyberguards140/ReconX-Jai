class TenancyCore:
    @staticmethod
    def validate_isolation(user_tenant_id: str, resource_tenant_id: str) -> bool:
        return user_tenant_id == resource_tenant_id
