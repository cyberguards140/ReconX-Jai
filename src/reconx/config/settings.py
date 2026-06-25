import os
import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = "ReconX"
    env: str = "development"
    debug: bool = False
    auto_reload: bool = False
    secure_cookies: bool = False


class DatabaseSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///reconx.database"


class SecuritySettings(BaseModel):
    jwt_secret: str = "CHANGE_ME"


class PluginSettings(BaseModel):
    dir: str = "plugins"


class LoggingSettings(BaseModel):
    level: str = "INFO"


class DockerSettings(BaseModel):
    enabled: bool = False


class Settings(BaseSettings):
    # Core app fields mapped flat for ENV override
    app_name: str = Field("ReconX", alias="APP_NAME")
    app_env: str = Field("development", alias="APP_ENV")
    debug: bool = Field(False, alias="DEBUG")
    auto_reload: bool = Field(False, alias="AUTO_RELOAD")
    secure_cookies: bool = Field(False, alias="SECURE_COOKIES")
    database_url: str = Field("sqlite+aiosqlite:///reconx.database", alias="DATABASE_URL")
    jwt_secret: str = Field("CHANGE_ME", alias="JWT_SECRET")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    project_id: str = Field("default", alias="PROJECT_ID")
    plugin_timeout: int = Field(120, ge=10, le=3600, alias="PLUGIN_TIMEOUT")

    @property
    def get_jwt_secret(self) -> str:
        if self.jwt_secret == "CHANGE_ME":
            if self.app_env == "production":
                raise ValueError("JWT_SECRET cannot be 'CHANGE_ME' in production!")
            import secrets
            return secrets.token_urlsafe(32)
        return self.jwt_secret
    workflow_timeout: int = Field(300, ge=10, le=3600, alias="WORKFLOW_TIMEOUT")
    workflow_directory: str = Field("src/reconx/workflows", alias="WORKFLOW_DIRECTORY")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def app(self) -> AppSettings:
        return AppSettings(
            name=self.app_name,
            env=self.app_env,
            debug=self.debug,
            auto_reload=self.auto_reload,
            secure_cookies=self.secure_cookies,
        )

    @property
    def database(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url)

    @property
    def security(self) -> SecuritySettings:
        return SecuritySettings(jwt_secret=self.get_jwt_secret)

    @property
    def logging(self) -> LoggingSettings:
        return LoggingSettings(level=self.log_level)

    @property
    def plugins(self) -> PluginSettings:
        return PluginSettings()


def load_settings() -> Settings:
    env = os.getenv("RECONX_ENV", "development")
    config_file = Path(f"config/{env}.yaml")

    kwargs = {}
    if config_file.exists():
        with open(config_file, "r") as f:
            yaml_config = yaml.safe_load(f) or {}

            # Map nested yaml to flat fields
            app_cfg = yaml_config.get("app", {})
            if "name" in app_cfg:
                kwargs["app_name"] = app_cfg["name"]
            if "env" in app_cfg:
                kwargs["app_env"] = app_cfg["env"]
            if "debug" in app_cfg:
                kwargs["debug"] = app_cfg["debug"]
            if "auto_reload" in app_cfg:
                kwargs["auto_reload"] = app_cfg["auto_reload"]
            if "secure_cookies" in app_cfg:
                kwargs["secure_cookies"] = app_cfg["secure_cookies"]

            db_cfg = yaml_config.get("database", {})
            if "url" in db_cfg:
                kwargs["database_url"] = db_cfg["url"]

            log_cfg = yaml_config.get("logging", {})
            if "level" in log_cfg:
                kwargs["log_level"] = log_cfg["level"]

    return Settings(**kwargs)


settings = load_settings()
