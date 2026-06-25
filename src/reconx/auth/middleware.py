import inspect
from functools import wraps
from fastapi import Request, HTTPException, status
from reconx.auth.identity import IdentityContext
from reconx.auth.authorization import authorize
from typing import Callable, Any

def require_permission(permission: str):
    """
    Decorator to enforce permission checks on FastAPI endpoints.
    The endpoint must include `request: Request` in its signature.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail="Request object not found for permission validation. Ensure 'request: Request' is in the endpoint signature."
                )
                
            identity: IdentityContext = getattr(request.state, "identity", None)
            if not identity:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
                
            is_allowed, reason = authorize(identity, permission)
            if not is_allowed:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=reason)
                
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(role: str):
    """
    Decorator to enforce role checks on FastAPI endpoints.
    The endpoint must include `request: Request` in its signature.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
                        
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail="Request object not found for role validation. Ensure 'request: Request' is in the endpoint signature."
                )
                
            identity: IdentityContext = getattr(request.state, "identity", None)
            if not identity:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
                
            if not identity.is_super_admin and role not in identity.roles:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requires role: {role}")
                
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response
from reconx.auth.jwt_manager import verify_token
from reconx.auth.session_manager import validate_session
from reconx.auth.identity import IdentityContext
from reconx.database.session import async_session_factory

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = verify_token(token)
                session_id = payload.get("session_id")
                
                # validate session
                async with async_session_factory() as session:
                    if session_id and await validate_session(session, session_id):
                        identity = IdentityContext(
                            user_id=payload.get("sub"),
                            tenant_id=payload.get("tenant_id"),
                            roles=payload.get("roles", []),
                            permissions=payload.get("permissions", []),
                            session_id=session_id,
                            ip_address=request.client.host if request.client else None,
                            user_agent=request.headers.get("user-agent")
                        )
                        request.state.identity = identity
                        
                        from reconx.enterprise.isolation.tenant_context import set_current_tenant_id, set_is_super_admin
                        set_current_tenant_id(identity.tenant_id)
                        set_is_super_admin(identity.is_super_admin)
            except Exception as e:
                # Token invalid or session invalid
                pass
                
        response = await call_next(request)
        return response
