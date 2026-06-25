import pytest
from reconx.auth.identity import IdentityContext
from reconx.auth.authorization import authorize
from reconx.auth.policies import allow
from reconx.auth.jwt_manager import create_access_token, verify_token

def test_identity_context_super_admin():
    identity = IdentityContext(
        user_id="123",
        tenant_id="tenant-1",
        roles=["SUPER_ADMIN"],
        permissions=[]
    )
    assert identity.is_super_admin is True

def test_authorize_super_admin():
    identity = IdentityContext(
        user_id="123",
        tenant_id="tenant-1",
        roles=["SUPER_ADMIN"],
        permissions=[]
    )
    is_allowed, reason = authorize(identity, "any.permission")
    assert is_allowed is True

def test_authorize_missing_permission():
    identity = IdentityContext(
        user_id="123",
        tenant_id="tenant-1",
        roles=["VIEWER"],
        permissions=["asset.read"]
    )
    is_allowed, reason = authorize(identity, "asset.create")
    assert is_allowed is False
    assert "Missing required permission" in reason

def test_authorize_tenant_isolation():
    identity = IdentityContext(
        user_id="123",
        tenant_id="tenant-1",
        roles=["ANALYST"],
        permissions=["asset.read"]
    )
    
    resource = {"tenant_id": "tenant-2"}
    is_allowed, reason = authorize(identity, "asset.read", resource)
    assert is_allowed is False
    assert "Blocked by ABAC policy or Tenant isolation rules" in reason

def test_authorize_abac_analyst_delete():
    identity = IdentityContext(
        user_id="123",
        tenant_id="tenant-1",
        roles=["ANALYST"],
        permissions=["asset.delete"]
    )
    
    # Analysts cannot perform deletion, even if they have the permission
    is_allowed, reason = authorize(identity, "asset.delete")
    assert is_allowed is False

def test_jwt_generation_and_validation():
    token = create_access_token(
        user_id="123",
        tenant_id="tenant-1",
        roles=["VIEWER"],
        permissions=["asset.read"],
        session_id="session-1"
    )
    
    payload = verify_token(token)
    assert payload["sub"] == "123"
    assert payload["tenant_id"] == "tenant-1"
    assert "VIEWER" in payload["roles"]
    assert "asset.read" in payload["permissions"]
    assert payload["session_id"] == "session-1"

def test_verify_token_invalid():
    with pytest.raises(ValueError, match="Invalid token"):
        verify_token("invalid.token.here")
