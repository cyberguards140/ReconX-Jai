import os
import jwt
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

ALGORITHM = "HS256"
# In a real enterprise system, you would load these from a secure vault or env vars.
# We fallback to a default secure-ish secret for backward compatibility or local dev.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-reconx-enterprise-key-change-in-prod")

def create_access_token(
    user_id: str, 
    tenant_id: Optional[str], 
    roles: List[str], 
    permissions: List[str], 
    session_id: str
) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id) if tenant_id else None,
        "roles": roles,
        "permissions": permissions,
        "session_id": str(session_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: str, tenant_id: Optional[str]) -> Dict[str, Any]:
    import uuid
    expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.now(timezone.utc) + expires_delta
    jti = str(uuid.uuid4())
    
    to_encode = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id) if tenant_id else None,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": jti,
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": encoded_jwt, "jti": jti, "exp": expire}

def verify_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
