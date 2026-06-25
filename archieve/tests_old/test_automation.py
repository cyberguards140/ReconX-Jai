import pytest
from reconx.modules.automation.scheduler import AutomationSchedulerCore
from reconx.modules.automation.workflow_engine import AutomationWorkflowCore
from reconx.modules.automation.triggers import TriggerEngine
from reconx.modules.automation.jobs import JobDefinition
from reconx.modules.automation.monitoring import MonitoringCore
from reconx.services.scheduler import SchedulerService
from reconx.services.workflow_engine import WorkflowEngineService
from reconx.services.alert_engine import AlertEngineService
from reconx.services.monitoring_engine import MonitoringEngineService
from reconx.services.job_queue import JobQueueService

def test_automation_scheduler():
    assert AutomationSchedulerCore.is_due("Hourly", "") == True
    assert AutomationSchedulerCore.is_due("Hourly", "2023-01-01T12:00:00") == True

def test_automation_workflow():
    tasks = AutomationWorkflowCore.get_workflow_tasks("QuickRecon")
    assert "DNS" in tasks
    assert "Subdomains" in tasks

def test_automation_triggers():
    assert TriggerEngine.should_trigger_alert("NewFinding", "Critical") == True
    assert TriggerEngine.should_trigger_alert("NewFinding", "Low") == False

def test_automation_jobs():
    job = JobDefinition("QuickRecon")
    assert job.job_type == "QuickRecon"
    job_dict = job.to_dict()
    assert job_dict["status"] == "Pending"

def test_automation_monitoring():
    old = ["a1", "a2"]
    new = ["a2", "a3"]
    diff = MonitoringCore.diff_assets(old, new)
    assert "a3" in diff["added"]
    assert "a1" in diff["removed"]

def test_alert_engine_service():
    alert = AlertEngineService.process_event("NewFinding", "High")
    assert alert["alert"] == True
    assert alert["severity"] == "High"

def test_monitoring_engine_service():
    events = MonitoringEngineService.analyze_changes(["a1"], ["a1", "a2"])
    assert len(events) == 1
    assert events[0]["type"] == "Added"
    assert events[0]["asset"] == "a2"

def test_job_queue_service():
    queue = JobQueueService()
    queue.enqueue({"job_type": "QuickRecon"})
    job = queue.execute_next()
    assert job is not None
    assert job["status"] == "Completed"
    assert queue.execute_next() is None
