from reconx.modules.enterprise.api import APICore


class APIGatewayService:
    @staticmethod
    def authenticate(token: str, stored_hash: str) -> bool:
        return APICore.validate_token(token, stored_hash)
