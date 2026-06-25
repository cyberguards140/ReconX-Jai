import pytest
from reconx.modules.enterprise.tenancy import TenancyCore
from reconx.modules.enterprise.rbac import RBACCore
from reconx.modules.enterprise.api import APICore
from reconx.modules.enterprise.integrations import IntegrationsCore
from reconx.modules.enterprise.audit import AuditCore
from reconx.services.tenant_manager import TenantManagerService
from reconx.services.user_manager import UserManagerService
from reconx.services.team_manager import TeamManagerService
from reconx.services.rbac import RBACService
from reconx.services.api_gateway import APIGatewayService
from reconx.services.audit_log import AuditLogService
from reconx.services.integration_manager import IntegrationManagerService
from reconx.services.webhooks import WebhookService

def test_enterprise_tenancy():
    assert TenancyCore.validate_isolation("t1", "t1") == True
    assert TenancyCore.validate_isolation("t1", "t2") == False

def test_enterprise_rbac():
    assert RBACCore.check_permission("Viewer", "View_Assets") == True
    assert RBACCore.check_permission("Viewer", "Run_Jobs") == False
    assert RBACCore.check_permission("Operator", "Run_Jobs") == True

def test_enterprise_api_auth():
    token = "secret-token"
    hashed = APICore.hash_token(token)
    assert APICore.validate_token(token, hashed) == True
    assert APICore.validate_token("wrong", hashed) == False

def test_enterprise_integrations():
    payload = IntegrationsCore.format_slack_payload("Alert!")
    assert payload["text"] == "Alert!"

def test_enterprise_audit():
    log = AuditCore.format_log("u1", "Login")
    assert log["user_id"] == "u1"
    assert log["action"] == "Login"
    assert "timestamp" in log

def test_tenant_manager_service():
    assert TenantManagerService.verify_access("t1", "t2") == False

def test_user_manager_service():
    um = UserManagerService()
    um.add_user({"user_id": "u1"})
    assert len(um.users) == 1

def test_team_manager_service():
    tm = TeamManagerService()
    tm.add_team({"team_id": "team1"})
    assert len(tm.teams) == 1

def test_rbac_service():
    assert RBACService.authorize("Admin", "Manage_Users") == True

def test_api_gateway_service():
    token = "test"
    hashed = APICore.hash_token(token)
    assert APIGatewayService.authenticate(token, hashed) == True

def test_audit_log_service():
    audit = AuditLogService()
    audit.log_action("u1", "Export")
    assert len(audit.logs) == 1
    assert audit.logs[0]["action"] == "Export"

def test_integration_manager_service():
    payload = IntegrationManagerService.prepare_slack_alert("Hi")
    assert payload["text"] == "Hi"

def test_webhook_service():
    hook = WebhookService.trigger("NewFinding", {"risk": "High"})
    assert hook["event"] == "NewFinding"
    assert hook["status"] == "sent"
