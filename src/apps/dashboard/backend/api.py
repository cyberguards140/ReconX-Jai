import os
import sys

from flask import Blueprint, jsonify, request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from core.legacy_core.analytics_db import (
    ExecutiveMetric,
    ExposureMetric,
    ForecastData,
    HistoricalSnapshot,
    RiskMetric,
    TrendData,
)
from core.legacy_core.analytics_db import SessionLocal as AnalyticsSession
from core.legacy_core.argument_engine import ArgumentEngine
from core.legacy_core.auth_db import (
    ActivityLog,
    ApprovalRequest,
    AuditLog,
    Organization,
    Role,
    Team,
)
from core.legacy_core.auth_db import SessionLocal as AuthSession
from core.legacy_core.campaign_db import (
    AssessmentScope,
    Campaign,
    CampaignMilestone,
    CampaignTask,
    Engagement,
    Evidence,
)
from core.legacy_core.campaign_db import SessionLocal as CampaignSession
from core.legacy_core.case_db import Artifact, Case, CaseReview
from core.legacy_core.case_db import Investigation as CaseInvestigation
from core.legacy_core.case_db import SessionLocal as CaseSession
from core.legacy_core.cloud_db import CloudAsset, IAMEntity, PublicExposure, StorageBucket
from core.legacy_core.cloud_db import SessionLocal as CloudSession
from core.legacy_core.config_manager import ConfigManager
from core.legacy_core.distributed_db import Agent, Cluster, DistributedJob, Node, NodeHealth
from core.legacy_core.distributed_db import SessionLocal as DistSession
from core.legacy_core.execution_engine import ExecutionEngine
from core.legacy_core.exposure_db import (
    Exposure,
    Ownership,
    RemediationAction,
    RiskReduction,
    RiskScore,
    SecurityPosture,
    SLAPolicy,
)
from core.legacy_core.exposure_db import SessionLocal as ExposureSession
from core.legacy_core.finding_db import Finding, RiskScore
from core.legacy_core.finding_db import SessionLocal as FindingSession
from core.legacy_core.graph_db import (
    AttackPath,
    GraphEntity,
    GraphRelationship,
    Investigation,
)
from core.legacy_core.graph_db import SessionLocal as GraphSession
from core.legacy_core.intelligence_db import AssetTimeline
from core.legacy_core.intelligence_db import SessionLocal as IntelSession
from core.legacy_core.inventory_manager import InventoryManager
from core.legacy_core.job_manager import JobManager
from core.legacy_core.plugin_db import ConnectorRegistry, Plugin, ThemeRegistry
from core.legacy_core.plugin_db import SessionLocal as PluginSession
from core.legacy_core.profile_manager import ProfileManager
from core.legacy_core.project_db import Campaign, Project, ScanProfile, Target
from core.legacy_core.project_db import SessionLocal as ProjectSession
from core.legacy_core.project_manager import ProjectManager
from core.legacy_core.report_db import Report as ReportDB
from core.legacy_core.report_db import SessionLocal as ReportSession
from core.legacy_core.screenshot_db import OCRResult, Screenshot, VisualChange, VisualFinding
from core.legacy_core.screenshot_db import SessionLocal as ScreenSession
from core.legacy_core.session import SessionManager
from core.legacy_core.threat_db import (
    ASNData,
    CVEData,
    ExposureEvent,
    IOCData,
    PassiveDNS,
    ReputationData,
)
from core.legacy_core.threat_db import SessionLocal as ThreatSession
from core.legacy_core.tool_registry import ToolRegistry
from core.legacy_core.validator import Validator
from core.legacy_core.web_db import Secret, Technology, WebAsset
from core.legacy_core.web_db import SessionLocal as WebSession
from operations.runbooks.doctor.doctor_engine import DoctorEngine
from operations.runbooks.doctor.repair_engine import RepairEngine
from platform_core.task_engine.pipelines.pipeline_manager import PipelineManager

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/health")
def health():
    return jsonify({"status": "online"})


@api_bp.route("/api/projects", methods=["GET"])
def list_projects():
    projects = ProjectManager.list_projects()
    return jsonify(projects)


@api_bp.route("/api/project", methods=["GET"])
def current_project():
    session = SessionManager()
    return jsonify({"project": session.current_project or "None", "id": session.project_id})


@api_bp.route("/api/project/create", methods=["POST"])
def create_project():
    data = request.json or {}
    success = ProjectManager.create_project(data.get("name"), data.get("description", ""))
    if success:
        return jsonify({"status": "created", "name": data.get("name")})
    return jsonify({"error": "Failed"}), 400


@api_bp.route("/api/project/delete", methods=["DELETE"])
def delete_project():
    data = request.json or {}
    name = data.get("name")
    session = SessionManager()
    if session.current_project == name:
        session.clear()
    if ProjectManager.delete_project(name):
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Failed"}), 500


@api_bp.route("/api/project/switch", methods=["POST"])
def switch_project():
    name = (request.json or {}).get("name")
    proj = ProjectManager.get_project(name)
    if proj:
        session = SessionManager()
        session.set_project(name, proj["id"])
        return jsonify({"status": "switched"})
    return jsonify({"error": "Not found"}), 404


@api_bp.route("/api/dashboard/status")
def status():
    return jsonify({"running": True})


# --- Registry Endpoints ---


@api_bp.route("/api/categories", methods=["GET"])
def list_categories():
    return jsonify(ToolRegistry.get_categories())


@api_bp.route("/api/tools", methods=["GET"])
def list_tools():
    return jsonify(ToolRegistry.get_tools())


@api_bp.route("/api/tools/<tool_id>", methods=["GET"])
@api_bp.route("/api/tools/<tool_id>/schema", methods=["GET"])
def get_tool(tool_id):
    t = ToolRegistry.get_tool(tool_id)
    if t:
        return jsonify(t)
    return jsonify({"error": "Not found"}), 404


@api_bp.route("/api/tools/<tool_id>/arguments", methods=["GET"])
def get_tool_arguments(tool_id):
    return jsonify(ToolRegistry.get_tool_arguments(tool_id))


@api_bp.route("/api/tools/<tool_id>/status", methods=["GET"])
def get_tool_status(tool_id):
    return jsonify({"status": ToolRegistry.get_tool_status(tool_id)})


# --- Stage 5 Dynamic Engine Endpoints ---


@api_bp.route("/api/tools/<tool_id>/profiles", methods=["GET"])
def get_tool_profiles(tool_id):
    return jsonify(ProfileManager.get_profiles(tool_id))


@api_bp.route("/api/tools/<tool_id>/config", methods=["GET"])
def get_config(tool_id):
    return jsonify(ConfigManager.load_config(tool_id))


@api_bp.route("/api/tools/<tool_id>/config", methods=["POST"])
def save_config(tool_id):
    data = request.json or {}
    if ConfigManager.save_config(tool_id, data):
        return jsonify({"status": "saved"})
    return jsonify({"error": "Failed to save"}), 500


@api_bp.route("/api/tools/<tool_id>/validate", methods=["POST"])
def validate_config(tool_id):
    data = request.json or {}
    target = data.get("target", "")
    if not Validator.validate_argument("target", target):
        return jsonify({"valid": False, "error": "Invalid target format"})
    return jsonify({"valid": True})


@api_bp.route("/api/tools/<tool_id>/command", methods=["POST"])
def generate_command(tool_id):
    data = request.json or {}
    target = data.get("target", "")
    config = data.get("config", {})
    cmd = ArgumentEngine.generate_command(tool_id, target, config)
    return jsonify({"command": cmd})


# --- Execution Endpoints ---


@api_bp.route("/api/jobs/create", methods=["POST"])
def create_job():
    data = request.json or {}
    tool_id = data.get("tool_id")
    target = data.get("target", "")
    config = data.get("config", {})

    session = SessionManager()
    project_id = session.current_project
    if not project_id:
        return jsonify({"error": "No active project"}), 400

    cmd = ArgumentEngine.generate_command(tool_id, target, config)
    if not cmd:
        return jsonify({"error": "Failed to build command"}), 400

    job_id = ExecutionEngine.queue_job(tool_id, project_id, target, cmd)
    return jsonify({"status": "queued", "job_id": job_id})


@api_bp.route("/api/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    job = JobManager.get_job(job_id)
    if job:
        return jsonify(job)
    return jsonify({"error": "Not found"}), 404


@api_bp.route("/api/jobs/<job_id>/stop", methods=["POST"])
def stop_job(job_id):
    if ExecutionEngine.stop_job(job_id):
        return jsonify({"status": "stopped"})
    return jsonify({"error": "Failed to stop"}), 500


@api_bp.route("/api/jobs/running", methods=["GET"])
def get_running_jobs():
    return jsonify(JobManager.get_jobs_by_status("running"))


# --- Inventory Endpoints ---


@api_bp.route("/api/assets", methods=["GET"])
def get_assets():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    return jsonify(InventoryManager.get_assets_by_project(session.current_project))


@api_bp.route("/api/assets/<asset_type>", methods=["GET"])
def get_assets_by_type(asset_type):
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    # Note: simple router, if it matches domains/ports/services
    a_type = asset_type[:-1] if asset_type.endswith("s") else asset_type
    return jsonify(InventoryManager.get_assets_by_project(session.current_project, a_type))


@api_bp.route("/api/stats", methods=["GET"])
def get_stats():
    session = SessionManager()
    if not session.current_project:
        return jsonify({})
    return jsonify(InventoryManager.get_stats(session.current_project))


# --- Recon Pipeline Endpoints ---


@api_bp.route("/api/recon/pipelines", methods=["GET"])
def get_pipelines():
    return jsonify(PipelineManager.get_pipelines())


@api_bp.route("/api/recon/run", methods=["POST"])
def run_pipeline():
    data = request.json or {}
    name = data.get("pipeline_name")
    target = data.get("target")
    session = SessionManager()
    project_id = session.current_project
    if not project_id:
        return jsonify({"error": "No active project"}), 400

    job_id = PipelineManager.start_pipeline(name, project_id, target)
    if job_id:
        return jsonify({"status": "started", "job_id": job_id})
    return jsonify({"error": "Failed to start pipeline"}), 400


# --- Findings Endpoints ---


@api_bp.route("/api/findings", methods=["GET"])
def get_findings():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = FindingSession()
    findings = db.query(Finding).filter(Finding.project_id == session.current_project).all()
    res = [{"id": f.id, "title": f.title, "severity": f.severity, "tool": f.tool} for f in findings]
    db.close()
    return jsonify(res)


@api_bp.route("/api/findings/risk", methods=["GET"])
def get_findings_risk():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = FindingSession()
    findings = db.query(Finding).filter(Finding.project_id == session.current_project).all()
    # Mocking risk aggregation
    res = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        s = f.severity.lower()
        if s in res:
            res[s] += 1
    db.close()
    return jsonify(res)


# --- Web Asset Endpoints ---


@api_bp.route("/api/web/<asset_type>", methods=["GET"])
def get_web_assets(asset_type):
    # maps to urls, endpoints, javascript, parameters
    # normalize type
    if asset_type == "javascript":
        t = "js_file"
    elif asset_type == "parameters":
        t = "parameter"
    elif asset_type == "endpoints":
        t = "endpoint"
    else:
        t = "url"

    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = WebSession()
    assets = (
        db.query(WebAsset)
        .filter(WebAsset.project_id == session.current_project, WebAsset.asset_type == t)
        .all()
    )
    res = [{"id": a.id, "value": a.value, "host": a.host, "status": a.status} for a in assets]
    db.close()
    return jsonify(res)


@api_bp.route("/api/web/secrets", methods=["GET"])
def get_web_secrets():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = WebSession()
    secs = db.query(Secret).filter(Secret.project_id == session.current_project).all()
    res = [{"id": s.id, "category": s.category, "value": s.value} for s in secs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/web/technologies", methods=["GET"])
def get_web_technologies():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = WebSession()
    techs = db.query(Technology).filter(Technology.project_id == session.current_project).all()
    res = [{"id": t.id, "name": t.name, "host": t.host} for t in techs]
    db.close()
    return jsonify(res)


# --- Cloud Asset Endpoints ---


@api_bp.route("/api/cloud/assets", methods=["GET"])
def get_cloud_assets():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = CloudSession()
    assets = db.query(CloudAsset).filter(CloudAsset.project_id == session.current_project).all()
    res = [
        {
            "id": a.id,
            "provider": a.provider,
            "name": a.name,
            "resource_type": a.resource_type,
            "public": a.public,
        }
        for a in assets
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/cloud/storage", methods=["GET"])
def get_cloud_storage():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = CloudSession()
    buckets = (
        db.query(StorageBucket).filter(StorageBucket.project_id == session.current_project).all()
    )
    res = [
        {
            "id": b.id,
            "provider": b.provider,
            "name": b.name,
            "public": b.public,
            "object_count": b.object_count,
        }
        for b in buckets
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/cloud/iam", methods=["GET"])
def get_cloud_iam():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = CloudSession()
    entities = db.query(IAMEntity).filter(IAMEntity.project_id == session.current_project).all()
    res = [
        {"id": e.id, "provider": e.provider, "entity_type": e.entity_type, "name": e.name}
        for e in entities
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/cloud/exposures", methods=["GET"])
def get_cloud_exposures():
    session = SessionManager()
    if not session.current_project:
        return jsonify([])
    db = CloudSession()
    exps = (
        db.query(PublicExposure).filter(PublicExposure.project_id == session.current_project).all()
    )
    res = [
        {"id": e.id, "asset_id": e.asset_id, "finding": e.finding, "severity": e.severity}
        for e in exps
    ]
    db.close()
    return jsonify(res)


# --- Doctor Endpoints ---


@api_bp.route("/api/doctor/scan", methods=["POST", "GET"])
def doctor_scan():
    report = DoctorEngine.scan()
    return jsonify(report)


@api_bp.route("/api/doctor/status", methods=["GET"])
def doctor_status():
    report = DoctorEngine.scan()
    return jsonify({"status": report["status"]})


@api_bp.route("/api/doctor/missing", methods=["GET"])
def doctor_missing():
    report = DoctorEngine.scan()
    return jsonify({"missing": report["missing_tools"]})


@api_bp.route("/api/doctor/repair", methods=["POST"])
def doctor_repair():
    data = request.json or {}
    tool = data.get("tool")
    if not tool:
        return jsonify({"error": "No tool specified"}), 400
    res = RepairEngine.repair(tool)
    return jsonify({"status": "repaired" if res else "failed", "tool": tool})


@api_bp.route("/api/doctor/updates", methods=["GET"])
def doctor_updates():
    # Mock update status
    return jsonify({"updates_available": 0, "tools": []})


# --- Project Endpoints ---


@api_bp.route("/api/projects", methods=["GET"])
def get_projects():
    db = ProjectSession()
    projects = db.query(Project).all()
    res = [
        {"id": p.id, "name": p.name, "description": p.description, "status": p.status}
        for p in projects
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/profiles", methods=["GET"])
def get_profiles():
    db = ProjectSession()
    profiles = db.query(ScanProfile).all()
    res = [{"id": p.id, "name": p.name} for p in profiles]
    db.close()
    return jsonify(res)


@api_bp.route("/api/projects/<id>/targets", methods=["GET"])
def get_project_targets(id):
    db = ProjectSession()
    targets = db.query(Target).filter(Target.project_id == id).all()
    res = [{"id": t.id, "type": t.target_type, "value": t.value, "scope": t.scope} for t in targets]
    db.close()
    return jsonify(res)


@api_bp.route("/api/projects/<id>/campaigns", methods=["GET"])
def get_project_campaigns(id):
    db = ProjectSession()
    campaigns = db.query(Campaign).filter(Campaign.project_id == id).all()
    res = [{"id": c.id, "name": c.name, "status": c.status} for c in campaigns]
    db.close()
    return jsonify(res)


# --- Report Endpoints ---


@api_bp.route("/api/reports/generate", methods=["POST"])
def generate_report():
    data = request.json or {}
    rtype = data.get("type", "executive")
    session = SessionManager()
    if not session.project_id:
        return jsonify({"error": "No project open"}), 400

    from reporting.report_engine import ReportEngine

    rep_id = ReportEngine.generate_report(session.project_id, session.current_project, rtype)
    return jsonify({"status": "generated", "report_id": rep_id})


@api_bp.route("/api/reports", methods=["GET"])
def get_reports():
    session = SessionManager()
    if not session.project_id:
        return jsonify([])
    db = ReportSession()
    reps = db.query(ReportDB).filter(ReportDB.project_id == session.project_id).all()
    res = [
        {"id": r.id, "type": r.report_type, "version": r.version, "path": r.file_path} for r in reps
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/reports/evidence", methods=["POST"])
def generate_evidence():
    session = SessionManager()
    if not session.project_id:
        return jsonify({"error": "No project open"}), 400

    from reporting.evidence_packager import EvidencePackager

    path = EvidencePackager.create_package(session.project_id, session.current_project)
    return jsonify({"status": "generated", "path": path})


# --- Automation Endpoints ---


@api_bp.route("/api/workflows", methods=["GET"])
def get_workflows():
    session = SessionManager()
    if not session.project_id:
        return jsonify([])
    from automation.workflow_engine import WorkflowEngine

    res = WorkflowEngine.get_workflows(session.project_id)
    return jsonify(res)


@api_bp.route("/api/workflows/schedule", methods=["POST"])
def schedule_workflow():
    data = request.json or {}
    w_id = data.get("workflow_id")
    freq = data.get("frequency")
    time = data.get("time")
    from automation.scheduler import SchedulerEngine

    job_id = SchedulerEngine.schedule_job(w_id, freq, time)
    return jsonify({"status": "scheduled", "job_id": job_id})


@api_bp.route("/api/jobs", methods=["GET"])
def get_jobs():
    from automation.queue_manager import QueueManager

    res = QueueManager.list_queue()
    return jsonify(res)


@api_bp.route("/api/alerts", methods=["GET"])
def get_alerts():
    session = SessionManager()
    if not session.project_id:
        return jsonify([])
    from automation.alert_manager import AlertManager

    res = AlertManager.get_unread(session.project_id)
    return jsonify(res)


# --- Intelligence Endpoints ---


@api_bp.route("/api/assets/<id>", methods=["GET"])
def get_asset(id):
    from intelligence.intelligence_center import IntelligenceCenter

    res = IntelligenceCenter.get_asset_profile(id)
    if not res:
        return jsonify({"error": "Asset not found"}), 404
    return jsonify(res)


@api_bp.route("/api/assets/<id>/timeline", methods=["GET"])
def get_asset_timeline(id):
    db = IntelSession()
    events = (
        db.query(AssetTimeline)
        .filter(AssetTimeline.asset_id == id)
        .order_by(AssetTimeline.timestamp.desc())
        .all()
    )
    res = [{"event": e.event_type, "message": e.message, "time": e.timestamp} for e in events]
    db.close()
    return jsonify(res)


@api_bp.route("/api/graph/<id>", methods=["GET"])
def get_asset_graph(id):
    from intelligence.relationship_engine import RelationshipEngine

    res = RelationshipEngine.get_graph(id)
    return jsonify(res)


@api_bp.route("/api/search", methods=["GET"])
def search_assets():
    q = request.args.get("q", "")
    from intelligence.search_engine import SearchEngine

    res = SearchEngine.search(q)
    return jsonify(res)


@api_bp.route("/api/search/suggestions", methods=["GET"])
def search_suggestions():
    # Provide quick autocomplete suggestions based on assets
    return jsonify([])


# --- Screenshot Endpoints ---


@api_bp.route("/api/screenshots/capture", methods=["POST"])
def capture_screenshot():
    data = request.json or {}
    url = data.get("url")
    asset_id = data.get("asset_id")
    session = SessionManager()
    if not session.project_id:
        return jsonify({"error": "No project open"}), 400

    from screenshots.screenshot_manager import ScreenshotManager

    s_id = ScreenshotManager.process_asset(session.current_project, asset_id, url)
    return jsonify({"status": "captured", "screenshot_id": s_id})


@api_bp.route("/api/screenshots/<asset_id>", methods=["GET"])
def get_asset_screenshots(asset_id):
    db = ScreenSession()
    shots = db.query(Screenshot).filter(Screenshot.asset_id == asset_id).all()
    res = [{"id": s.id, "path": s.path, "time": s.timestamp} for s in shots]
    db.close()
    return jsonify(res)


@api_bp.route("/api/screenshots/findings", methods=["GET"])
def get_visual_findings():
    db = ScreenSession()
    findings = db.query(VisualFinding).all()
    res = [{"id": f.id, "asset_id": f.asset_id, "type": f.finding_type} for f in findings]
    db.close()
    return jsonify(res)


@api_bp.route("/api/screenshots/ocr", methods=["GET"])
def get_ocr_results():
    db = ScreenSession()
    results = db.query(OCRResult).all()
    res = [{"id": r.id, "asset_id": r.asset_id, "text": r.text} for r in results]
    db.close()
    return jsonify(res)


@api_bp.route("/api/screenshots/changes", methods=["GET"])
def get_visual_changes():
    db = ScreenSession()
    changes = db.query(VisualChange).all()
    res = [{"id": c.id, "asset_id": c.asset_id, "score": c.change_score} for c in changes]
    db.close()
    return jsonify(res)


# --- Threat Intelligence Endpoints ---


@api_bp.route("/api/threats", methods=["GET"])
def get_threats():
    # Aggregate threat endpoint
    return jsonify({"status": "active"})


@api_bp.route("/api/cves", methods=["GET"])
def get_cves():
    db = ThreatSession()
    cves = db.query(CVEData).all()
    res = [{"id": c.id, "cve": c.cve, "severity": c.severity, "cvss": c.cvss} for c in cves]
    db.close()
    return jsonify(res)


@api_bp.route("/api/iocs", methods=["GET"])
def get_iocs():
    db = ThreatSession()
    iocs = db.query(IOCData).all()
    res = [{"id": i.id, "type": i.ioc_type, "value": i.value, "source": i.source} for i in iocs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/reputation", methods=["GET"])
def get_reputation():
    db = ThreatSession()
    reps = db.query(ReputationData).all()
    res = [
        {"id": r.id, "asset_id": r.asset_id, "status": r.status, "score": r.reputation_score}
        for r in reps
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/asn", methods=["GET"])
def get_asn_data():
    db = ThreatSession()
    asns = db.query(ASNData).all()
    res = [{"id": a.id, "asn": a.asn, "org": a.organization, "country": a.country} for a in asns]
    db.close()
    return jsonify(res)


@api_bp.route("/api/passive-dns", methods=["GET"])
def get_passive_dns():
    db = ThreatSession()
    pdns = db.query(PassiveDNS).all()
    res = [{"id": p.id, "domain": p.domain, "historical_ip": p.historical_ip} for p in pdns]
    db.close()
    return jsonify(res)


@api_bp.route("/api/exposure-events", methods=["GET"])
def get_exposure_events():
    db = ThreatSession()
    exps = db.query(ExposureEvent).all()
    res = [{"id": e.id, "asset_id": e.asset_id, "event": e.event_type} for e in exps]
    db.close()
    return jsonify(res)


# --- Authentication & Governance Endpoints ---


@api_bp.route("/api/auth/login", methods=["POST"])
def auth_login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    from core.auth.authentication import AuthenticationEngine

    success, msg = AuthenticationEngine.login(username, password)
    if success:
        return jsonify({"status": "authenticated", "session_id": msg})
    return jsonify({"error": msg}), 401


@api_bp.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    # Simulated logout
    return jsonify({"status": "logged_out"})


@api_bp.route("/api/auth/me", methods=["GET"])
def get_current_user():
    return jsonify({"username": "admin", "role": "Super Admin"})


@api_bp.route("/api/roles", methods=["GET"])
def get_roles():
    db = AuthSession()
    roles = db.query(Role).all()
    res = [{"id": r.id, "name": r.name} for r in roles]
    db.close()
    return jsonify(res)


@api_bp.route("/api/teams", methods=["GET"])
def get_teams():
    db = AuthSession()
    teams = db.query(Team).all()
    res = [{"id": t.id, "name": t.name} for t in teams]
    db.close()
    return jsonify(res)


@api_bp.route("/api/organizations", methods=["GET"])
def get_orgs():
    db = AuthSession()
    orgs = db.query(Organization).all()
    res = [{"id": o.id, "name": o.name} for o in orgs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/audit", methods=["GET"])
def get_audit_logs():
    db = AuthSession()
    logs = db.query(AuditLog).all()
    res = [{"id": l.id, "event": l.event, "timestamp": l.timestamp} for l in logs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/activity", methods=["GET"])
def get_activity_logs():
    db = AuthSession()
    logs = db.query(ActivityLog).all()
    res = [{"id": l.id, "action": l.action, "timestamp": l.timestamp} for l in logs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/approvals", methods=["GET"])
def get_approval_requests():
    db = AuthSession()
    reqs = db.query(ApprovalRequest).all()
    res = [{"id": r.id, "action": r.action, "status": r.status} for r in reqs]
    db.close()
    return jsonify(res)


# --- Plugin & Extension Endpoints ---


@api_bp.route("/api/plugins", methods=["GET"])
def get_plugins():
    db = PluginSession()
    plugins = db.query(Plugin).all()
    res = [{"id": p.id, "name": p.name, "version": p.version, "status": p.status} for p in plugins]
    db.close()
    return jsonify(res)


@api_bp.route("/api/plugins/install", methods=["POST"])
def install_plugin():
    data = request.json or {}
    pkg_name = data.get("package_name")
    return jsonify({"status": "installed", "package": pkg_name})


@api_bp.route("/api/plugins/enable", methods=["POST"])
def enable_plugin():
    data = request.json or {}
    plugin_id = data.get("plugin_id")
    from platform_core.plugin_engine.plugin_manager import PluginManager

    PluginManager.enable_plugin(plugin_id)
    return jsonify({"status": "enabled"})


@api_bp.route("/api/marketplace", methods=["GET"])
def get_marketplace():
    from platform_core.plugin_engine.marketplace_engine import MarketplaceEngine

    catalog = MarketplaceEngine.fetch_catalog()
    return jsonify(catalog)


@api_bp.route("/api/connectors", methods=["GET"])
def get_connectors():
    db = PluginSession()
    conn = db.query(ConnectorRegistry).all()
    res = [{"id": c.id, "name": c.connector_name, "enabled": c.enabled} for c in conn]
    db.close()
    return jsonify(res)


@api_bp.route("/api/themes", methods=["GET"])
def get_themes():
    db = PluginSession()
    themes = db.query(ThemeRegistry).all()
    res = [{"id": t.id, "theme": t.theme_name, "active": t.is_active} for t in themes]
    db.close()
    return jsonify(res)


# --- Distributed Architecture Endpoints ---


@api_bp.route("/api/nodes", methods=["GET"])
def get_nodes():
    db = DistSession()
    nodes = db.query(Node).all()
    res = [
        {"id": n.id, "hostname": n.hostname, "status": n.status, "type": n.node_type} for n in nodes
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/agents", methods=["GET"])
def get_agents():
    db = DistSession()
    agents = db.query(Agent).all()
    res = [{"id": a.id, "node_id": a.node_id, "version": a.version} for a in agents]
    db.close()
    return jsonify(res)


@api_bp.route("/api/clusters", methods=["GET"])
def get_clusters():
    db = DistSession()
    clusters = db.query(Cluster).all()
    res = [{"id": c.id, "name": c.name, "type": c.cluster_type} for c in clusters]
    db.close()
    return jsonify(res)


@api_bp.route("/api/jobs/distributed", methods=["GET"])
def get_distributed_jobs():
    db = DistSession()
    jobs = db.query(DistributedJob).all()
    res = [{"id": j.id, "job": j.job_name, "status": j.status} for j in jobs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/nodes/metrics", methods=["GET"])
def get_node_metrics():
    db = DistSession()
    metrics = db.query(NodeHealth).all()
    res = [{"node_id": m.node_id, "cpu": m.cpu_usage, "state": m.health_state} for m in metrics]
    db.close()
    return jsonify(res)


@api_bp.route("/api/agent/register", methods=["POST"])
def register_agent():
    data = request.json or {}
    hostname = data.get("hostname", "unknown-node")
    node_type = data.get("node_type", "Worker")
    token = data.get("token", "dummy-token")

    from recon.internet_scale.distributed.registry.node_registry import NodeRegistry

    node_id = NodeRegistry.register_node(hostname, node_type, token)
    return jsonify({"status": "registered", "node_id": node_id})


@api_bp.route("/api/agent/heartbeat", methods=["POST"])
def agent_heartbeat():
    data = request.json or {}
    node_id = data.get("node_id")
    cpu = data.get("cpu", 0.0)
    ram = data.get("ram", 0.0)

    from recon.internet_scale.distributed.health.health_monitor import HealthMonitor

    state = HealthMonitor.process_heartbeat(node_id, cpu, ram, 0.0, 0.0)
    return jsonify({"status": "received", "state": state})


@api_bp.route("/api/agent/results", methods=["POST"])
def agent_results():
    # Simulated endpoint where remote nodes push recon data
    return jsonify({"status": "results_collected"})


# --- Analytics & Executive Intelligence Endpoints ---


@api_bp.route("/api/analytics/metrics", methods=["GET"])
def get_analytics_metrics():
    db = AnalyticsSession()
    # Mocking generic metrics route to pull recent snapshots
    snaps = db.query(HistoricalSnapshot).all()
    res = [
        {
            "id": s.id,
            "assets": s.total_assets,
            "findings": s.total_findings,
            "date": s.snapshot_date,
        }
        for s in snaps
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/analytics/trends", methods=["GET"])
def get_analytics_trends():
    db = AnalyticsSession()
    trends = db.query(TrendData).all()
    res = [
        {"id": t.id, "category": t.trend_category, "delta": t.delta_value, "desc": t.description}
        for t in trends
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/analytics/risk", methods=["GET"])
def get_analytics_risk():
    db = AnalyticsSession()
    risks = db.query(RiskMetric).all()
    res = [
        {"id": r.id, "project": r.project_id, "score": r.risk_score, "date": r.timestamp}
        for r in risks
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/analytics/exposure", methods=["GET"])
def get_analytics_exposure():
    db = AnalyticsSession()
    exposures = db.query(ExposureMetric).all()
    res = [
        {"id": e.id, "project": e.project_id, "score": e.exposure_score, "date": e.timestamp}
        for e in exposures
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/analytics/forecast", methods=["GET"])
def get_analytics_forecast():
    db = AnalyticsSession()
    forecasts = db.query(ForecastData).all()
    res = [
        {
            "id": f.id,
            "category": f.forecast_category,
            "target": f.projected_value,
            "date": f.target_date,
        }
        for f in forecasts
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/analytics/kpis", methods=["GET"])
def get_analytics_kpis():
    db = AnalyticsSession()
    kpis = db.query(ExecutiveMetric).all()
    res = [{"id": k.id, "metric": k.metric_name, "value": k.metric_value} for k in kpis]
    db.close()
    return jsonify(res)


@api_bp.route("/api/analytics/history", methods=["GET"])
def get_analytics_history():
    db = AnalyticsSession()
    snaps = db.query(HistoricalSnapshot).order_by(HistoricalSnapshot.snapshot_date.desc()).all()
    res = [{"id": s.id, "assets": s.total_assets, "date": s.snapshot_date} for s in snaps]
    db.close()
    return jsonify(res)


# --- Knowledge Graph & Investigation Endpoints ---


@api_bp.route("/api/graph/entities", methods=["GET"])
def get_graph_entities():
    db = GraphSession()
    entities = db.query(GraphEntity).all()
    res = [{"id": e.id, "type": e.entity_type, "value": e.entity_value} for e in entities]
    db.close()
    return jsonify(res)


@api_bp.route("/api/graph/relationships", methods=["GET"])
def get_graph_relationships():
    db = GraphSession()
    rels = db.query(GraphRelationship).all()
    res = [
        {
            "id": r.id,
            "source": r.source_id,
            "target": r.target_id,
            "type": r.relation_type,
            "confidence": r.confidence_score,
        }
        for r in rels
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/graph/search", methods=["GET"])
def search_graph():
    return jsonify({"status": "search_active", "results": []})


@api_bp.route("/api/investigations", methods=["GET"])
def get_investigations():
    db = GraphSession()
    invs = db.query(Investigation).all()
    res = [{"id": i.id, "title": i.title, "status": i.status} for i in invs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/attack-paths", methods=["GET"])
def get_attack_paths():
    db = GraphSession()
    paths = db.query(AttackPath).all()
    res = [{"id": p.id, "risk": p.risk_score, "path": p.path_details} for p in paths]
    db.close()
    return jsonify(res)


@api_bp.route("/api/graph/analytics", methods=["GET"])
def get_graph_analytics():
    # Return connected assets mock
    return jsonify({"most_connected": [{"asset": "example.com", "connections": 15}]})


# --- Continuous Exposure Management (CEM) Endpoints ---


@api_bp.route("/api/exposures", methods=["GET"])
def get_exposures():
    db = ExposureSession()
    exps = db.query(Exposure).all()
    res = [
        {
            "id": e.id,
            "asset": e.asset_id,
            "type": e.exposure_type,
            "severity": e.severity,
            "status": e.status,
        }
        for e in exps
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/risk", methods=["GET"])
def get_risk_scores():
    db = ExposureSession()
    risks = db.query(RiskScore).all()
    res = [{"id": r.id, "exposure_id": r.exposure_id, "score": r.score} for r in risks]
    db.close()
    return jsonify(res)


@api_bp.route("/api/posture", methods=["GET"])
def get_security_posture():
    db = ExposureSession()
    postures = db.query(SecurityPosture).all()
    res = [
        {"id": p.id, "project": p.project_id, "score": p.score, "grade": p.grade} for p in postures
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/remediation", methods=["GET"])
def get_remediation():
    db = ExposureSession()
    rems = db.query(RemediationAction).all()
    res = [{"id": r.id, "exposure_id": r.exposure_id, "status": r.status} for r in rems]
    db.close()
    return jsonify(res)


@api_bp.route("/api/ownership", methods=["GET"])
def get_ownership():
    db = ExposureSession()
    owners = db.query(Ownership).all()
    res = [{"id": o.id, "asset_id": o.asset_id, "owner": o.owner} for o in owners]
    db.close()
    return jsonify(res)


@api_bp.route("/api/sla", methods=["GET"])
def get_sla_policies():
    db = ExposureSession()
    slas = db.query(SLAPolicy).all()
    res = [{"severity": s.severity, "deadline_days": s.deadline_days} for s in slas]
    db.close()
    return jsonify(res)


@api_bp.route("/api/risk-reduction", methods=["GET"])
def get_risk_reduction():
    db = ExposureSession()
    reds = db.query(RiskReduction).all()
    res = [{"id": r.id, "project": r.project_id, "reduction": r.reduction_percentage} for r in reds]
    db.close()
    return jsonify(res)


# --- Campaign Management & Operations Endpoints ---


@api_bp.route("/api/campaigns", methods=["GET", "POST"])
def manage_campaigns_api():
    if request.method == "POST":
        data = request.json or {}
        from campaigns.campaign_manager import CampaignManager

        c_id = CampaignManager.create_campaign(
            data.get("name", "New Campaign"), data.get("type", "External ASM")
        )
        return jsonify({"status": "created", "campaign_id": c_id})
    else:
        db = CampaignSession()
        camps = db.query(Campaign).all()
        res = [
            {"id": c.id, "name": c.name, "type": c.campaign_type, "status": c.status} for c in camps
        ]
        db.close()
        return jsonify(res)


@api_bp.route("/api/engagements", methods=["GET"])
def get_engagements():
    db = CampaignSession()
    engs = db.query(Engagement).all()
    res = [
        {"id": e.id, "name": e.engagement_name, "client": e.client, "status": e.status}
        for e in engs
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/campaigns/scope", methods=["GET"])
def get_scopes():
    db = CampaignSession()
    scopes = db.query(AssessmentScope).all()
    res = [
        {"id": s.id, "campaign": s.campaign_id, "target": s.target, "status": s.status}
        for s in scopes
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/tasks", methods=["GET"])
def get_tasks():
    db = CampaignSession()
    tasks = db.query(CampaignTask).all()
    res = [
        {"id": t.id, "name": t.task_name, "status": t.status, "assignee": t.assigned_to}
        for t in tasks
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/milestones", methods=["GET"])
def get_milestones():
    db = CampaignSession()
    stones = db.query(CampaignMilestone).all()
    res = [{"id": m.id, "name": m.milestone_name, "status": m.status} for m in stones]
    db.close()
    return jsonify(res)


@api_bp.route("/api/evidence", methods=["GET"])
def get_evidence():
    db = CampaignSession()
    evs = db.query(Evidence).all()
    res = [{"id": e.id, "type": e.evidence_type, "path": e.file_path} for e in evs]
    db.close()
    return jsonify(res)


@api_bp.route("/api/campaigns/analytics", methods=["GET"])
def get_campaign_analytics():
    return jsonify({"assets_discovered": 1450, "findings": 89, "coverage": 95.0})


# --- Case Management & Investigations Endpoints ---


@api_bp.route("/api/cases", methods=["GET", "POST"])
def manage_cases_api():
    if request.method == "POST":
        data = request.json or {}
        from cases.case_manager import CaseManager

        c_id = CaseManager.create_case(
            data.get("title", "New Case"), data.get("type", "Threat Investigation")
        )
        return jsonify({"status": "created", "case_id": c_id})
    else:
        db = CaseSession()
        cases = db.query(Case).all()
        res = [
            {"id": c.id, "title": c.title, "type": c.case_type, "status": c.status} for c in cases
        ]
        db.close()
        return jsonify(res)


@api_bp.route("/api/cases/investigations", methods=["GET"])
def get_case_investigations():
    db = CaseSession()
    invs = db.query(CaseInvestigation).all()
    res = [
        {"id": i.id, "case": i.case_id, "name": i.investigation_name, "owner": i.owner}
        for i in invs
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/artifacts", methods=["GET"])
def get_artifacts():
    db = CaseSession()
    arts = db.query(Artifact).all()
    res = [
        {"id": a.id, "name": a.artifact_name, "type": a.artifact_type, "path": a.file_path}
        for a in arts
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/reviews", methods=["GET"])
def get_reviews():
    db = CaseSession()
    revs = db.query(CaseReview).all()
    res = [
        {"id": r.id, "case": r.case_id, "reviewer": r.reviewer, "status": r.status} for r in revs
    ]
    db.close()
    return jsonify(res)


@api_bp.route("/api/cases/analytics", methods=["GET"])
def get_cases_analytics():
    from cases.analytics import InvestigationAnalytics

    return jsonify(InvestigationAnalytics.get_metrics())
