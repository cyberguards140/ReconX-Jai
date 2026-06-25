import hashlib


class APICore:
    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def validate_token(provided_token: str, stored_hash: str) -> bool:
        return APICore.hash_token(provided_token) == stored_hash
