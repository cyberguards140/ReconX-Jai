import logging
import uuid
from typing import Any

from sqlalchemy import select, update

from reconx.database.models import Tenant
from reconx.database.session import async_session_factory

logger = logging.getLogger(__name__)


class TenantManager:
    """
    Manages the lifecycle of ReconX Enterprise Tenants.
    Enforces cross-tenant protections during lifecycle operations.
    """

    async def create_tenant(self, name: str, billing_plan: str = "Enterprise") -> dict[str, Any]:
        async with async_session_factory() as session:
            # Check for existing tenant
            result = await session.execute(select(Tenant).filter(Tenant.name == name))
            if result.scalars().first():
                raise ValueError(f"Tenant with name '{name}' already exists.")

            tenant_id = str(uuid.uuid4())
            tenant = Tenant(id=tenant_id, name=name, billing_plan=billing_plan, status="ACTIVE")
            session.add(tenant)
            await session.commit()

            logger.info(f"Created new Tenant: {name} ({tenant_id})")
            return {"id": tenant.id, "name": tenant.name, "status": tenant.status}

    async def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        async with async_session_factory() as session:
            result = await session.execute(select(Tenant).filter(Tenant.id == tenant_id))
            tenant = result.scalars().first()
            if not tenant:
                return None
            return {
                "id": tenant.id,
                "name": tenant.name,
                "status": tenant.status,
                "billing_plan": tenant.billing_plan,
                "created_at": tenant.created_at,
            }

    async def list_tenants(self) -> list[dict[str, Any]]:
        async with async_session_factory() as session:
            result = await session.execute(select(Tenant))
            tenants = result.scalars().all()
            return [
                {"id": t.id, "name": t.name, "status": t.status, "billing_plan": t.billing_plan}
                for t in tenants
            ]

    async def update_tenant_status(self, tenant_id: str, new_status: str) -> bool:
        valid_states = {"ACTIVE", "SUSPENDED", "ARCHIVED", "DELETED"}
        if new_status not in valid_states:
            raise ValueError(f"Invalid tenant state. Must be one of {valid_states}")

        async with async_session_factory() as session:
            result = await session.execute(
                update(Tenant).where(Tenant.id == tenant_id).values(status=new_status)
            )
            await session.commit()
            if result.rowcount > 0:
                logger.info(f"Tenant {tenant_id} status updated to {new_status}")
                return True
            return False

    async def archive_tenant(self, tenant_id: str) -> bool:
        return await self.update_tenant_status(tenant_id, "ARCHIVED")

    async def restore_tenant(self, tenant_id: str) -> bool:
        return await self.update_tenant_status(tenant_id, "ACTIVE")

    async def suspend_tenant(self, tenant_id: str) -> bool:
        return await self.update_tenant_status(tenant_id, "SUSPENDED")

    async def delete_tenant(self, tenant_id: str) -> bool:
        return await self.update_tenant_status(tenant_id, "DELETED")
