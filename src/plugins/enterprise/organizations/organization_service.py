import logging
import uuid
from typing import Any

from sqlalchemy import select

from data.database.models import BusinessUnit, Department, Organization
from data.database.session import async_session_factory

logger = logging.getLogger(__name__)


class OrganizationService:
    """
    Manages the Enterprise Organization Hierarchy.
    (Tenant -> Organization -> BusinessUnit -> Department -> Project)
    """

    async def create_organization(
        self, name: str, tenant_id: str, description: str | None = None
    ) -> str:
        async with async_session_factory() as session:
            org_id = str(uuid.uuid4())
            org = Organization(id=org_id, name=name, description=description, tenant_id=tenant_id)
            session.add(org)
            await session.commit()
            logger.info(f"Created Organization: {name}")
            return org_id

    async def create_business_unit(self, name: str, org_id: str, tenant_id: str) -> str:
        async with async_session_factory() as session:
            bu_id = str(uuid.uuid4())
            bu = BusinessUnit(id=bu_id, name=name, organization_id=org_id, tenant_id=tenant_id)
            session.add(bu)
            await session.commit()
            return bu_id

    async def create_department(self, name: str, bu_id: str, tenant_id: str) -> str:
        async with async_session_factory() as session:
            dept_id = str(uuid.uuid4())
            dept = Department(id=dept_id, name=name, business_unit_id=bu_id, tenant_id=tenant_id)
            session.add(dept)
            await session.commit()
            return dept_id

    async def get_organization_hierarchy(self, tenant_id: str) -> list[dict[str, Any]]:
        """
        Retrieves the complete nested hierarchy for a specific tenant.
        This provides a top-down view of the enterprise structure.
        """
        async with async_session_factory() as session:
            result = await session.execute(
                select(Organization).filter(Organization.tenant_id == tenant_id)
            )
            orgs = result.scalars().unique().all()

            hierarchy = []
            for org in orgs:
                # Eagerly load BusinessUnits and Departments
                # In a high-perf scenario, this should use joinedload/selectinload
                result_bu = await session.execute(
                    select(BusinessUnit).filter(BusinessUnit.organization_id == org.id)
                )
                bus = result_bu.scalars().unique().all()

                bu_list = []
                for bu in bus:
                    result_dept = await session.execute(
                        select(Department).filter(Department.business_unit_id == bu.id)
                    )
                    depts = result_dept.scalars().unique().all()

                    bu_list.append(
                        {
                            "id": bu.id,
                            "name": bu.name,
                            "departments": [{"id": d.id, "name": d.name} for d in depts],
                        }
                    )

                hierarchy.append(
                    {
                        "id": org.id,
                        "name": org.name,
                        "description": org.description,
                        "business_units": bu_list,
                    }
                )

            return hierarchy
