from core.config.secrets import validate_secrets
from core.config.settings import settings
from core.legacy_core.errors import ConfigurationError


def run_startup_checks():
    if not settings.database.url:
        raise ConfigurationError("DATABASE_URL must be configured.")

    if not settings.security.jwt_secret:
        raise ConfigurationError("JWT_SECRET must be securely configured.")

    import os
    if os.getenv("ENCRYPTION_MASTER_KEY") == "uE4F7jC9gLzRkXbQyNpVt3H+V8s2M6wY0zF/K5Xq/8Y=" and settings.app.env == "production":
        raise ConfigurationError("ENCRYPTION_MASTER_KEY cannot use the default value in production.")

    valid_envs = {"development", "testing", "staging", "production"}
    if settings.app.env not in valid_envs:
        raise ConfigurationError(f"APP_ENV invalid. Allowed: {valid_envs}")

    if settings.logging.level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ConfigurationError("LOG_LEVEL must be a valid logging level.")

    validate_secrets(settings)
