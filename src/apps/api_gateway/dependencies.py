"""FastAPI dependency injection functions for ReconX API routes."""

from fastapi import Depends, HTTPException, Request, status


async def get_current_user(request: Request) -> dict:
    """Extract and validate the current authenticated user from the request.

    Returns a dict with user info. Raises 401 if not authenticated.
    """
    # TODO: Implement JWT token validation against auth service
    user = getattr(request.state, "user", None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user


async def get_current_identity(request: Request) -> dict:
    """Extract the current identity context (user or service account)."""
    identity = getattr(request.state, "identity", None)
    if identity is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identity context required",
        )
    return identity


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """Dependency that requires the current user to have admin role."""
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user


def require_permission(permission: str):
    """Factory that returns a dependency requiring a specific permission."""

    async def _check_permission(user: dict = Depends(get_current_user)) -> dict:
        user_permissions = user.get("permissions", [])
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required",
            )
        return user

    return _check_permission
