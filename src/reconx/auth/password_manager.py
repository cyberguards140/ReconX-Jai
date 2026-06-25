import hashlib


class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        # In a real enterprise system, use bcrypt or argon2. Using SHA256 for simulated portability.
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordManager.hash_password(plain_password) == hashed_password
