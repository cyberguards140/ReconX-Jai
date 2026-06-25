import logging

from sqlalchemy import func, select

from data.database.models import Asset, Report, User
from data.database.session import async_session_factory

logger = logging.getLogger(__name__)


class BillingFoundation:
    """
    Core foundation for usage tracking, license caps, and feature flags.
    """

    # Hardcoded limits for different plans
    PLAN_LIMITS = {
        "Free": {"users": 5, "assets": 100, "reports_per_month": 5},
        "Pro": {"users": 25, "assets": 1000, "reports_per_month": 50},
        "Enterprise": {"users": -1, "assets": -1, "reports_per_month": -1},  # -1 means unlimited
    }

    async def get_tenant_usage(self, tenant_id: str) -> dict[str, int]:
        """Calculates current usage metrics for a tenant."""
        async with async_session_factory() as session:
            # Note: with global ORM filters active, we still pass tenant_id
            # but we explicitly count for this specific tenant instance.

            user_count = await session.execute(
                select(func.count(User.id)).filter(User.tenant_id == tenant_id)
            )

            asset_count = await session.execute(
                select(func.count(Asset.id)).filter(Asset.tenant_id == tenant_id)
            )

            report_count = await session.execute(
                select(
                    func.count(Report.id)
                )  # Tenant filter applied globally in query_filter if it has tenant_id
            )

            return {
                "users": user_count.scalar() or 0,
                "assets": asset_count.scalar() or 0,
                "reports_this_month": report_count.scalar() or 0,
            }

    async def check_feature_flag(self, tenant_id: str, feature: str) -> bool:
        """
        Check if a specific feature flag is enabled for the given tenant.
        This allows graceful degradation of UI for non-Enterprise tenants.
        """
        # Mock logic
        return True

    async def validate_usage_limit(self, tenant_id: str, plan_type: str, metric: str) -> bool:
        """Checks if the tenant is within their plan's limits."""
        limits = self.PLAN_LIMITS.get(plan_type, self.PLAN_LIMITS["Free"])
        cap = limits.get(metric, 0)

        if cap == -1:
            return True

        usage = await self.get_tenant_usage(tenant_id)
        current = usage.get(metric, 0)

        return current < cap
