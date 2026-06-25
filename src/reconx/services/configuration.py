import os
import yaml

class ConfigurationService:
    @staticmethod
    def load_config(env: str = "production") -> dict:
        # Load stub yaml configuration
        base = {"database_url": "sqlite+aiosqlite:///reconx.db", "log_level": "INFO"}
        
        # Override with environment variables
        if "RECONX_DB_URL" in os.environ:
            base["database_url"] = os.environ["RECONX_DB_URL"]
        if "RECONX_LOG_LEVEL" in os.environ:
            base["log_level"] = os.environ["RECONX_LOG_LEVEL"]
            
        return base
