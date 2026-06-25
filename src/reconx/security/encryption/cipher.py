import base64
import logging
import os

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

logger = logging.getLogger(__name__)


class EncryptionManager:
    """
    AES-256-GCM Authenticated Encryption for data-at-rest.
    Ensures confidentiality and integrity of field-level database data (e.g., API keys, OAuth tokens).
    """

    def __init__(self):
        # In production, this key should be injected from Vault or AWS KMS
        # 32 bytes base64 encoded by default for AES-256
        self.master_key_b64 = os.getenv(
            "ENCRYPTION_MASTER_KEY", "uE4F7jC9gLzRkXbQyNpVt3H+V8s2M6wY0zF/K5Xq/8Y="
        )
        self.key = base64.b64decode(self.master_key_b64)

        if len(self.key) != 32:
            logger.warning(
                "ENCRYPTION_MASTER_KEY is not 32 bytes. Encryption may fail or be insecure."
            )

        if HAS_CRYPTO:
            self.aesgcm = AESGCM(self.key)
        else:
            logger.warning("cryptography package not installed. Running in PLAINTEXT mock mode.")

    def encrypt(self, plaintext: str, associated_data: bytes = None) -> str:
        """
        Encrypts a string and returns a base64 encoded ciphertext including the nonce.
        Associated data can be a tenant_id to bind the ciphertext cryptographically to a specific tenant.
        """
        if not plaintext:
            return ""

        if not HAS_CRYPTO:
            return f"MOCK_ENC:{plaintext}"

        # GCM needs a 12-byte unique nonce per encryption
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated_data)

        # Prepend nonce to ciphertext for decryption
        payload = nonce + ciphertext
        return base64.b64encode(payload).decode("utf-8")

    def decrypt(self, encoded_payload: str, associated_data: bytes = None) -> str:
        """
        Decrypts a base64 encoded payload. Must provide the same associated_data used during encryption.
        """
        if not encoded_payload:
            return ""

        if not HAS_CRYPTO and encoded_payload.startswith("MOCK_ENC:"):
            return encoded_payload.replace("MOCK_ENC:", "")

        try:
            payload = base64.b64decode(encoded_payload.encode("utf-8"))
            nonce = payload[:12]
            ciphertext = payload[12:]

            plaintext = self.aesgcm.decrypt(nonce, ciphertext, associated_data)
            return plaintext.decode("utf-8")
        except Exception as e:
            logger.error(
                "Decryption failed. The data may be tampered with or the wrong key/AAD was used."
            )
            raise ValueError("Decryption failed") from e


encryption_manager = EncryptionManager()
