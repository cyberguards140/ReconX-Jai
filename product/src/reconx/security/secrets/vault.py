import os
import logging
from typing import Dict, Any, Optional

try:
    import hvac
    HAS_HVAC = True
except ImportError:
    HAS_HVAC = False

logger = logging.getLogger(__name__)

class VaultManager:
    """
    Enterprise Secrets Manager integrating with HashiCorp Vault.
    Provides automatic token renewal and transparent fallback to 
    environment variables for local development.
    """
    def __init__(self):
        self.url = os.getenv("VAULT_ADDR", "http://vault:8200")
        self.token = os.getenv("VAULT_TOKEN")
        self.client: Optional[hvac.Client] = None

        if HAS_HVAC and self.token:
            try:
                self.client = hvac.Client(url=self.url, token=self.token)
                if self.client.is_authenticated():
                    logger.info(f"Successfully authenticated with Vault at {self.url}")
                else:
                    logger.warning("Vault token is invalid.")
            except Exception as e:
                logger.error(f"Failed to connect to Vault: {e}")
        else:
            logger.warning("hvac not installed or VAULT_TOKEN not set. Running in insecure local mode.")

    def get_secret(self, path: str, default: Any = None) -> Dict[str, Any]:
        """
        Retrieves a secret payload from the KV v2 engine.
        Falls back to environment variables or `default` if Vault is inaccessible.
        """
        if self.client and self.client.is_authenticated():
            try:
                response = self.client.secrets.kv.v2.read_secret_version(path=path)
                return response['data']['data']
            except Exception as e:
                logger.error(f"Failed to read secret from path {path}: {e}")
        
        # Fallback to local environment mapping
        logger.debug(f"Falling back to local environment for secret path: {path}")
        return self._local_fallback(path, default)

    def _local_fallback(self, path: str, default: Any) -> Dict[str, Any]:
        if path == "database/credentials/postgres":
            return {
                "username": os.getenv("POSTGRES_USER", "reconx"),
                "password": os.getenv("POSTGRES_PASSWORD", "reconx_secure_pass")
            }
        elif path == "database/credentials/neo4j":
            return {
                "username": os.getenv("NEO4J_USER", "neo4j"),
                "password": os.getenv("NEO4J_PASSWORD", "reconx_secure_graph")
            }
        elif path == "auth/jwt":
            return {
                "secret_key": os.getenv("JWT_SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
            }
        return default or {}

# Global Vault Instance
vault_manager = VaultManager()
