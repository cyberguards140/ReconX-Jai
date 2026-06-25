import logging
from typing import Any

logger = logging.getLogger(__name__)

# Mocked settings store. In production, this would be a JSON column in Tenant table or a separate Settings table.
_tenant_settings_store: dict[str, dict[str, Any]] = {}


class SettingsManager:
    """
    Manages tenant-specific configuration, policies, and branding.
    """

    DEFAULT_SETTINGS = {
        "security": {
            "mfa_required": False,
            "session_timeout_minutes": 60,
            "password_expiration_days": 90,
        },
        "retention": {"audit_logs_days": 365, "incident_data_days": 730},
        "branding": {"logo_url": None, "primary_color": "#000000", "custom_theme_enabled": False},
    }

    async def get_tenant_settings(self, tenant_id: str) -> dict[str, Any]:
        """Retrieves tenant settings, falling back to defaults."""
        settings = _tenant_settings_store.get(tenant_id)
        if not settings:
            return self.DEFAULT_SETTINGS.copy()
        return settings

    async def update_tenant_settings(
        self, tenant_id: str, new_settings: dict[str, Any]
    ) -> dict[str, Any]:
        """Deep updates tenant settings."""
        current = await self.get_tenant_settings(tenant_id)

        # Simple merge for nested dicts
        for category, values in new_settings.items():
            if category in current and isinstance(current[category], dict):
                current[category].update(values)
            else:
                current[category] = values

        _tenant_settings_store[tenant_id] = current
        logger.info(f"Updated settings for tenant {tenant_id}")
        return current

    async def get_tenant_branding(self, tenant_id: str) -> dict[str, Any]:
        settings = await self.get_tenant_settings(tenant_id)
        return settings.get("branding", self.DEFAULT_SETTINGS["branding"])
